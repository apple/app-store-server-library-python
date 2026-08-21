# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import datetime
import hashlib
from typing import List, Optional

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import NameOID

WWDR_INTERMEDIATE_OID = '1.2.840.113635.100.6.2.1'
RECEIPT_SIGNER_OID = '1.2.840.113635.100.6.11.1'

SHA1_OID = '1.3.14.3.2.26'
SHA256_OID = '2.16.840.1.101.3.4.2.1'
SHA512_OID = '2.16.840.1.101.3.4.2.3'
RSA_ENCRYPTION_OID = '1.2.840.113549.1.1.1'
PKCS7_DATA_OID = '1.2.840.113549.1.7.1'
PKCS7_SIGNED_DATA_OID = '1.2.840.113549.1.7.2'
CONTENT_TYPE_OID = '1.2.840.113549.1.9.3'
MESSAGE_DIGEST_OID = '1.2.840.113549.1.9.4'
SIGNING_TIME_OID = '1.2.840.113549.1.9.5'

# The receipt digest, by the name hashlib knows it: the two Apple uses, plus one it does not for the allowlist
DIGESTS = {'sha1': (hashes.SHA1, SHA1_OID), 'sha256': (hashes.SHA256, SHA256_OID), 'sha512': (hashes.SHA512, SHA512_OID)}

DAY = datetime.timedelta(days=1)

def encode(tag: int, content: bytes) -> bytes:
    if len(content) < 0x80:
        return bytes([tag, len(content)]) + content
    length = len(content).to_bytes((len(content).bit_length() + 7) // 8, 'big')
    return bytes([tag, 0x80 | len(length)]) + length + content

def encode_integer(value: int) -> bytes:
    return encode(0x02, value.to_bytes(max(1, (value.bit_length() + 8) // 8), 'big'))

def encode_object_identifier(dotted: str) -> bytes:
    arcs = [int(arc) for arc in dotted.split('.')]
    body = bytearray([arcs[0] * 40 + arcs[1]])
    for arc in arcs[2:]:
        chunk = [arc & 0x7F]
        arc >>= 7
        while arc:
            chunk.append(0x80 | (arc & 0x7F))
            arc >>= 7
        body += bytes(reversed(chunk))
    return encode(0x06, bytes(body))

def encode_sequence(*parts: bytes) -> bytes:
    return encode(0x30, b''.join(parts))

def encode_set(*parts: bytes) -> bytes:
    return encode(0x31, b''.join(parts))

def encode_context(number: int, content: bytes) -> bytes:
    return encode(0xA0 | number, content)

def encode_segmented_octet_string(value: bytes, segment_size: int) -> bytes:
    """A constructed OCTET STRING, the shape BER splits a long value into and the one genuine receipts use."""
    return encode(0x24, b''.join(encode(0x04, value[offset:offset + segment_size]) for offset in range(0, len(value), segment_size)))

def encode_algorithm(oid: str) -> bytes:
    return encode_sequence(encode_object_identifier(oid), b'\x05\x00')

def encode_utc_time(when: datetime.datetime) -> bytes:
    return encode(0x17, when.astimezone(datetime.timezone.utc).strftime('%y%m%d%H%M%SZ').encode())

class AttributeSet:
    """
    Builds a receipt attribute SET, the shape both the receipt payload and the value of an in-app purchase
    attribute take. Each attribute is SEQUENCE { type INTEGER, version INTEGER, value OCTET STRING }.
    """
    def __init__(self):
        self._attributes: List[bytes] = []

    def string(self, attribute_type: int, value: str) -> 'AttributeSet':
        """An attribute whose value is a DER UTF8String, e.g. the bundle identifier."""
        return self.raw(attribute_type, encode(0x0C, value.encode('utf-8')))

    def date(self, attribute_type: int, value: str) -> 'AttributeSet':
        """An attribute whose value is a DER IA5String holding an RFC 3339 date."""
        return self.raw(attribute_type, encode(0x16, value.encode('ascii')))

    def integer(self, attribute_type: int, value: int) -> 'AttributeSet':
        """An attribute whose value is a DER INTEGER, e.g. a purchase quantity."""
        return self.raw(attribute_type, encode_integer(value))

    def raw(self, attribute_type: int, value: bytes) -> 'AttributeSet':
        """An attribute whose value bytes are used as-is, e.g. an opaque value or a nested SET."""
        self._attributes.append(encode_sequence(encode_integer(attribute_type), encode_integer(1), encode(0x04, value)))
        return self

    def build(self) -> bytes:
        return encode_set(*self._attributes)

class ReceiptCreator:
    """
    Generates a throwaway "Apple-like" RSA PKI (root, WWDR intermediate, receipt signing leaf) and CMS-signs
    synthetic legacy app receipts with it, so AppReceiptVerifier can be exercised without any real Apple key
    material or a checked-in receipt.
    """
    def __init__(self, chain: List[x509.Certificate], signing_key: rsa.RSAPrivateKey):
        # Leaf first, then intermediate, then root; a self-signed creator holds one entry
        self._chain = chain
        self._signing_key = signing_key

    def get_root_certificate(self) -> bytes:
        """The root of this chain, in the form the verifier's constructor accepts."""
        return self._chain[-1].public_bytes(serialization.Encoding.DER)

    def sign_receipt(self, payload: bytes, embedded_certificates: Optional[int] = None, signing_time: Optional[datetime.datetime] = None, signed_attributes: bool = True, digest: str = 'sha256', content_segment_size: Optional[int] = None) -> bytes:
        """
        CMS-signs the payload as encapsulated content, embedding the chain.

        :param embedded_certificates: How many certificates of the chain, starting at the leaf, to embed
        :param signing_time: The CMS signing time attribute, which an old receipt signed by a since expired
            certificate carries from when it was created
        :param signed_attributes: Whether the signer authenticates attributes and signs those instead of signing
            the payload directly, as Apple's own receipts do not
        :param digest: The digest the signer names and signs with, by its hashlib name
        :param content_segment_size: Encodes the payload as a constructed OCTET STRING of segments this size
        """
        embedded = self._chain[:embedded_certificates] if embedded_certificates is not None else self._chain
        algorithm, digest_oid = DIGESTS[digest]
        if signed_attributes:
            attributes = b''.join([
                encode_sequence(encode_object_identifier(CONTENT_TYPE_OID), encode_set(encode_object_identifier(PKCS7_DATA_OID))),
                encode_sequence(encode_object_identifier(SIGNING_TIME_OID), encode_set(encode_utc_time(signing_time if signing_time is not None else datetime.datetime.now(datetime.timezone.utc)))),
                encode_sequence(encode_object_identifier(MESSAGE_DIGEST_OID), encode_set(encode(0x04, hashlib.new(digest, payload).digest()))),
            ])
            # The signature covers the signed attributes as an explicit SET, not with their implicit [0] tag
            signature = self._signing_key.sign(encode_set(attributes), padding.PKCS1v15(), algorithm())
            attributes_field = [encode_context(0, attributes)]
        else:
            signature = self._signing_key.sign(payload, padding.PKCS1v15(), algorithm())
            attributes_field = []
        signer_info = encode_sequence(
            encode_integer(1),
            encode_sequence(self._chain[0].issuer.public_bytes(), encode_integer(self._chain[0].serial_number)),
            encode_algorithm(digest_oid),
            *attributes_field,
            encode_algorithm(RSA_ENCRYPTION_OID),
            encode(0x04, signature),
        )
        signed_data = encode_sequence(
            encode_integer(1),
            encode_set(encode_algorithm(digest_oid)),
            encode_sequence(encode_object_identifier(PKCS7_DATA_OID), encode_context(0, encode(0x04, payload) if content_segment_size is None else encode_segmented_octet_string(payload, content_segment_size))),
            encode_context(0, b''.join(certificate.public_bytes(serialization.Encoding.DER) for certificate in embedded)),
            encode_set(signer_info),
        )
        return encode_sequence(encode_object_identifier(PKCS7_SIGNED_DATA_OID), encode_context(0, signed_data))

def double_wrap(payload: bytes) -> bytes:
    """The extra OCTET STRING wrapper Xcode-generated receipts put around the payload."""
    return encode(0x04, payload)

def create_receipt_creator(receipt_signer_oid: bool = True, wwdr_intermediate_oid: bool = True, not_before: Optional[datetime.datetime] = None, not_after: Optional[datetime.datetime] = None) -> ReceiptCreator:
    """
    A chain carrying both Apple marker OIDs, by default with a validity window wide enough to cover any
    plausible receipt creation date; the chain of a receipt is evaluated at the date the receipt was created,
    not now.

    :param receipt_signer_oid: Whether the leaf carries the receipt-signing marker OID
    :param wwdr_intermediate_oid: Whether the intermediate carries the WWDR marker OID
    :param not_before: The start of the validity window of every certificate in the chain
    :param not_after: The end of the validity window of every certificate in the chain
    """
    not_before = days_ago(3650) if not_before is None else not_before
    not_after = in_one_year() if not_after is None else not_after
    root_key = _rsa_key()
    intermediate_key = _rsa_key()
    leaf_key = _rsa_key()
    root = _certificate('Test App Store Root CA', root_key.public_key(), 'Test App Store Root CA', root_key, True, None, not_before, not_after)
    intermediate = _certificate('Test WWDR CA', intermediate_key.public_key(), 'Test App Store Root CA', root_key, True, WWDR_INTERMEDIATE_OID if wwdr_intermediate_oid else None, not_before, not_after)
    leaf = _certificate('Test Receipt Signing', leaf_key.public_key(), 'Test WWDR CA', intermediate_key, False, RECEIPT_SIGNER_OID if receipt_signer_oid else None, not_before, not_after)
    return ReceiptCreator([leaf, intermediate, root], leaf_key)

def create_self_signed_receipt_creator() -> ReceiptCreator:
    """A single self-signed certificate, as an Xcode-generated receipt carries; such a receipt is never chain verified."""
    key = _rsa_key()
    certificate = _certificate('Test Xcode Receipt Signing', key.public_key(), 'Test Xcode Receipt Signing', key, False, RECEIPT_SIGNER_OID, days_ago(3650), in_one_year())
    return ReceiptCreator([certificate], key)

def days_ago(days: int) -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc) - days * DAY

def in_one_year() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc) + 365 * DAY

def _rsa_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)

def _certificate(subject: str, subject_key: rsa.RSAPublicKey, issuer: str, issuer_key: rsa.RSAPrivateKey, certificate_authority: bool, marker_oid: Optional[str], not_before: datetime.datetime, not_after: datetime.datetime) -> x509.Certificate:
    builder = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject)]))
        .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, issuer)]))
        .public_key(subject_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(not_before)
        .not_valid_after(not_after)
        .add_extension(x509.BasicConstraints(ca=certificate_authority, path_length=None), critical=True)
    )
    if marker_oid is not None:
        # The Apple marker extensions are non-critical and carry no value
        builder = builder.add_extension(x509.UnrecognizedExtension(x509.ObjectIdentifier(marker_oid), b'\x05\x00'), critical=False)
    return builder.sign(issuer_key, hashes.SHA256())
