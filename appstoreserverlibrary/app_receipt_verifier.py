# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import datetime
import hashlib
import hmac
import time
from base64 import b64decode, b64encode
from typing import Dict, List, NamedTuple, Optional, Tuple

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from .models.AppReceipt import AppReceipt
from .models.Environment import Environment
from .models.InAppPurchaseReceipt import InAppPurchaseReceipt

from .signed_data_verifier import _ChainVerifier, VerificationException, VerificationStatus

PKCS7_SIGNED_DATA_OID = "1.2.840.113549.1.7.2"
MESSAGE_DIGEST_OID = "1.2.840.113549.1.9.4"
SHA1_OID = "1.3.14.3.2.26"
SHA256_OID = "2.16.840.1.101.3.4.2.1"

ATTR_RECEIPT_TYPE = 0
ATTR_BUNDLE_ID = 2
ATTR_APP_VERSION = 3
ATTR_OPAQUE_VALUE = 4
ATTR_SHA1_HASH = 5
ATTR_CREATION_DATE = 12
ATTR_IN_APP = 17
ATTR_ORIGINAL_PURCHASE_DATE = 18
ATTR_ORIGINAL_APP_VERSION = 19
ATTR_EXPIRATION_DATE = 21

IAP_QUANTITY = 1701
IAP_PRODUCT_ID = 1702
IAP_TRANSACTION_ID = 1703
IAP_PURCHASE_DATE = 1704
IAP_ORIGINAL_TRANSACTION_ID = 1705
IAP_ORIGINAL_PURCHASE_DATE = 1706
IAP_EXPIRES_DATE = 1708
IAP_WEB_ORDER_LINE_ITEM_ID = 1711
IAP_CANCELLATION_DATE = 1712
IAP_IS_IN_INTRO_OFFER_PERIOD = 1719

# Only the digests Apple signs receipts with; the algorithm named by the signer
# is otherwise rejected rather than trusted.
_DIGESTS = {SHA1_OID: ('sha1', hashes.SHA1), SHA256_OID: ('sha256', hashes.SHA256)}

# Bounds on what is read before the receipt has been verified, so that a hostile receipt cannot make parsing
# expensive: the nesting a genuine receipt uses with room to spare, an object identifier wider than any real
# one, and the certificates a chain can hold.
MAXIMUM_ASN1_DEPTH = 32
MAXIMUM_OID_BYTES = 32
MAXIMUM_EMBEDDED_CERTIFICATES = 10

# Only explicit production values map to the Production environment; an unknown
# or missing receipt type maps to None and fails environment validation.
_ENVIRONMENT_BY_RECEIPT_TYPE = {
    'Production': Environment.PRODUCTION,
    'ProductionVPP': Environment.PRODUCTION,
    'ProductionSandbox': Environment.SANDBOX,
    'ProductionVPPSandbox': Environment.SANDBOX,
    'Xcode': Environment.XCODE,
    'LocalTesting': Environment.LOCAL_TESTING,
}

class AppReceiptVerifier:
    """
    A class providing utility methods for verifying and decoding legacy PKCS#7 App Store receipts, the app receipt
    used with the deprecated verifyReceipt endpoint.

    This is the validating counterpart to ReceiptUtility, which extracts without validation. The receipt's
    certificate chain is validated with the same chain verification used for JWS signed data, against the same
    caller-supplied Apple root certificates, and evaluated at the receipt's creation date so old receipts survive
    certificate rotations unless online checks are enabled.
    """
    def __init__(
        self,
        root_certificates: List[bytes],
        enable_online_checks: bool,
        environment: Environment,
        bundle_id: str,
    ):
        self._chain_verifier = _ChainVerifier(root_certificates)
        self._environment = environment
        self._bundle_id = bundle_id
        self._enable_online_checks = enable_online_checks

    def verify_and_decode_app_receipt(self, encoded_receipt: str) -> AppReceipt:
        """
        Verifies and decodes an app receipt, as obtained from a device
        See https://developer.apple.com/documentation/appstorereceipts

        :param encoded_receipt: The base64-encoded app receipt
        :return: The decoded receipt after verification
        :throws VerificationException: Thrown if the receipt could not be verified
        """
        try:
            try:
                # Whitespace is stripped rather than rejected, tolerating the line breaks base64 receipts
                # commonly pick up in transit
                receipt_der = b64decode(''.join(encoded_receipt.split()), validate=True)
            except (ValueError, TypeError, AttributeError) as e:
                raise VerificationException(VerificationStatus.VERIFICATION_FAILURE) from e
            signed_data = _parse_signed_data(receipt_der)
            # Parsed before signature verification only to learn the creation date (chain validity is anchored
            # at signing time); nothing from it is trusted until the chain and signature checks pass.
            receipt = _parse_receipt_payload(signed_data.content)
            if self._environment != Environment.XCODE and self._environment != Environment.LOCAL_TESTING:
                effective_date = time.time() if self._enable_online_checks or receipt.receiptCreationDate is None else receipt.receiptCreationDate // 1000
                signing_key = self._verify_chain(signed_data, effective_date)
                _verify_signature(signed_data, signing_key)
            # In the Xcode and LocalTesting environments the data is not signed by the App Store and signature
            # verification is skipped, but the bundle id and environment are still validated
            if receipt.bundleId != self._bundle_id:
                raise VerificationException(VerificationStatus.INVALID_APP_IDENTIFIER)
            if _ENVIRONMENT_BY_RECEIPT_TYPE.get(receipt.receiptType) != self._environment:
                raise VerificationException(VerificationStatus.INVALID_ENVIRONMENT)
            return receipt
        except VerificationException as e:
            raise e
        except Exception as e:
            raise VerificationException(VerificationStatus.VERIFICATION_FAILURE) from e

    def verify_and_extract_transaction_id(self, encoded_receipt: str) -> Optional[str]:
        """
        Verifies an app receipt and extracts a transaction id from its in-app purchases, the validated counterpart
        of ReceiptUtility.extract_transaction_id_from_app_receipt, with the same output contract

        :param encoded_receipt: The base64-encoded app receipt
        :return: A transaction id from the array of in-app purchases, None if the receipt contains no in-app purchases
        :throws VerificationException: Thrown if the receipt could not be verified
        """
        receipt = self.verify_and_decode_app_receipt(encoded_receipt)
        for purchase in receipt.inAppPurchases:
            if purchase.transactionId is not None:
                return purchase.transactionId
            if purchase.originalTransactionId is not None:
                return purchase.originalTransactionId
        return None

    def _verify_chain(self, signed_data: '_SignedData', effective_date: float) -> str:
        """
        Orders the receipt's embedded certificates as leaf, intermediate, root and hands them to the shared
        _ChainVerifier, which enforces the chain length, the WWDR intermediate OID and the receipt-signing leaf
        OID, and validates to the caller-supplied Apple roots.
        """
        # The embedded certificates are attacker-supplied and are parsed and ordered into a chain below, before
        # anything about the receipt has been verified, so a receipt carrying more of them than a chain can hold
        # is rejected here rather than assembled
        if len(signed_data.certificates) > MAXIMUM_EMBEDDED_CERTIFICATES:
            raise VerificationException(VerificationStatus.INVALID_CHAIN_LENGTH)
        try:
            certificates = [(der, x509.load_der_x509_certificate(der)) for der in signed_data.certificates]
        except Exception as e:
            raise VerificationException(VerificationStatus.INVALID_CERTIFICATE) from e
        ordered = [_find_signer_certificate(certificates, signed_data)]
        while len(ordered) < len(certificates):
            issuer = next((c for c in certificates if c not in ordered and c[1].subject == ordered[-1][1].issuer), None)
            if issuer is None:
                break
            ordered.append(issuer)
        return self._chain_verifier.verify_chain(
            [b64encode(der).decode() for der, _ in ordered], self._enable_online_checks, effective_date
        )

class _Element(NamedTuple):
    """One parsed ASN.1 element, as offsets into the buffer it was read from."""
    tag: int
    start: int
    content_start: int
    content_end: int
    end: int

class _Signer(NamedTuple):
    """The fields of a CMS SignerInfo this library uses."""
    issuer: Optional[bytes]
    serial_number: Optional[int]
    subject_key_identifier: Optional[bytes]
    digest_oid: str
    signed_attributes: Optional[bytes]
    signature: bytes

class _SignedData(NamedTuple):
    content: bytes
    certificates: List[bytes]
    signer: _Signer

def _read_element(data: bytes, offset: int, depth: int = 0) -> _Element:
    """Reads one BER/DER element, supporting the indefinite lengths genuine App Store receipts use."""
    # Finding the end of an indefinite-length element means walking everything inside it, and its parent walked
    # it too, so the work grows with the nesting depth. Genuine receipts nest a handful of levels; the bound
    # keeps a receipt built only to be deeply nested from being expensive to reject.
    if depth > MAXIMUM_ASN1_DEPTH:
        raise ValueError('ASN.1 element is nested too deeply')
    if offset + 2 > len(data):
        raise ValueError('Truncated ASN.1 element')
    tag = data[offset]
    if tag & 0x1F == 0x1F:
        raise ValueError('Multi-byte ASN.1 tags are not supported')
    position = offset + 2
    length = data[offset + 1]
    if length == 0x80:
        if not tag & 0x20:
            raise ValueError('Primitive ASN.1 element with an indefinite length')
        content_start = position
        while True:
            if position + 2 > len(data):
                raise ValueError('Unterminated indefinite-length ASN.1 element')
            if data[position] == 0x00 and data[position + 1] == 0x00:
                return _Element(tag, offset, content_start, position, position + 2)
            position = _read_element(data, position, depth + 1).end
    if length & 0x80:
        count = length & 0x7F
        if count > 4 or position + count > len(data):
            raise ValueError('Unsupported ASN.1 length')
        length = int.from_bytes(data[position:position + count], 'big')
        position += count
    if position + length > len(data):
        raise ValueError('ASN.1 length exceeds the available input')
    return _Element(tag, offset, position, position + length, position + length)

def _children(data: bytes, element: _Element, depth: int = 0) -> List[_Element]:
    children = []
    position = element.content_start
    while position < element.content_end:
        child = _read_element(data, position, depth + 1)
        # A child that runs past its parent is rejected rather than read, so a nested element can never be
        # interpreted from bytes outside the element that declares it
        if child.end > element.content_end:
            raise ValueError('ASN.1 element runs past the end of its parent')
        children.append(child)
        position = child.end
    return children

def _content(data: bytes, element: _Element) -> bytes:
    return data[element.content_start:element.content_end]

def _octets(data: bytes, element: _Element, what: str, depth: int = 0) -> bytes:
    """The value of an OCTET STRING, joining the segments BER splits long values into."""
    if element.tag & ~0x20 != 0x04:
        raise ValueError(what + ' is not an ASN.1 octet string')
    if not element.tag & 0x20:
        return _content(data, element)
    if depth > MAXIMUM_ASN1_DEPTH:
        raise ValueError('ASN.1 element is nested too deeply')
    return b''.join(_octets(data, child, what, depth + 1) for child in _children(data, element, depth))

def _decode_oid(data: bytes, element: _Element) -> str:
    body = _content(data, element)
    if not body or len(body) > MAXIMUM_OID_BYTES or body[-1] & 0x80:
        raise ValueError('Malformed ASN.1 object identifier')
    arcs = []
    value = 0
    for byte in body:
        value = value << 7 | (byte & 0x7F)
        if not byte & 0x80:
            arcs.append(value)
            value = 0
    first = arcs[0]
    if first < 80:
        leading = [first // 40, first % 40]
    else:
        leading = [2, first - 80]
    return '.'.join(str(arc) for arc in leading + arcs[1:])

def _expect(data: bytes, element: _Element, tag: int, what: str) -> _Element:
    if element.tag != tag:
        raise ValueError(what + ' has an unexpected ASN.1 tag')
    return element

def _parse_signed_data(receipt_der: bytes) -> _SignedData:
    content_info = _read_element(receipt_der, 0)
    # Parsing must exhaust the input, rejecting trailing bytes after the CMS blob
    if content_info.tag != 0x30 or content_info.end != len(receipt_der):
        raise ValueError('Receipt is not a PKCS#7 container')
    fields = _children(receipt_der, content_info)
    if len(fields) != 2 or _decode_oid(receipt_der, _expect(receipt_der, fields[0], 0x06, 'Content type')) != PKCS7_SIGNED_DATA_OID:
        raise ValueError('Receipt is not a PKCS#7 container')
    wrapped = _children(receipt_der, _expect(receipt_der, fields[1], 0xA0, 'Signed data'))
    if len(wrapped) != 1:
        raise ValueError('Receipt is not a PKCS#7 container')
    signed_data = _children(receipt_der, _expect(receipt_der, wrapped[0], 0x30, 'Signed data'))
    if len(signed_data) < 4:
        raise ValueError('Receipt is not a PKCS#7 container')
    content = _parse_encapsulated_content(receipt_der, _expect(receipt_der, signed_data[2], 0x30, 'Encapsulated content'))
    # Everything after the encapsulated content is optional but for the signer infos: the certificates and the
    # revocation lists carry context tags, so the SET among them is the signer infos
    optional = signed_data[3:]
    certificates = [receipt_der[child.start:child.end] for element in optional if element.tag == 0xA0 for child in _children(receipt_der, element)]
    signers = [child for element in optional if element.tag == 0x31 for child in _children(receipt_der, element)]
    if not signers:
        raise ValueError('Receipt has no signer info')
    return _SignedData(content, certificates, _parse_signer(receipt_der, signers[0]))

def _parse_encapsulated_content(data: bytes, encapsulated: _Element) -> bytes:
    fields = _children(data, encapsulated)
    if len(fields) < 2:
        raise ValueError('Receipt has no encapsulated payload')
    wrapped = _children(data, _expect(data, fields[1], 0xA0, 'Encapsulated payload'))
    if len(wrapped) != 1:
        raise ValueError('Receipt has no encapsulated payload')
    return _octets(data, wrapped[0], 'Encapsulated payload')

def _parse_signer(data: bytes, signer_info: _Element) -> _Signer:
    fields = _children(data, _expect(data, signer_info, 0x30, 'Signer info'))
    if len(fields) < 5:
        raise ValueError('Signer info has too few fields')
    issuer = None
    serial_number = None
    subject_key_identifier = None
    if fields[1].tag == 0x30:
        identifier = _children(data, fields[1])
        if len(identifier) != 2:
            raise ValueError('Malformed signer identifier')
        issuer = data[identifier[0].start:identifier[0].end]
        serial_number = int.from_bytes(_content(data, _expect(data, identifier[1], 0x02, 'Serial number')), 'big', signed=True)
    elif fields[1].tag == 0x80:
        subject_key_identifier = _content(data, fields[1])
    else:
        raise ValueError('Malformed signer identifier')
    digest_oid = _decode_oid(data, _expect(data, _children(data, _expect(data, fields[2], 0x30, 'Digest algorithm'))[0], 0x06, 'Digest algorithm'))
    signed_attributes = None
    remaining = fields[3:]
    if remaining[0].tag == 0xA0:
        signed_attributes = data[remaining[0].start:remaining[0].end]
        remaining = remaining[1:]
    if len(remaining) < 2:
        raise ValueError('Signer info has too few fields')
    signature = _octets(data, remaining[1], 'Signature')
    return _Signer(issuer, serial_number, subject_key_identifier, digest_oid, signed_attributes, signature)

def _find_signer_certificate(certificates: List[Tuple[bytes, x509.Certificate]], signed_data: _SignedData) -> Tuple[bytes, x509.Certificate]:
    for candidate in certificates:
        if signed_data.signer.subject_key_identifier is not None:
            try:
                key_identifier = candidate[1].extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value.digest
            except x509.ExtensionNotFound:
                continue
            if key_identifier == signed_data.signer.subject_key_identifier:
                return candidate
        elif candidate[1].serial_number == signed_data.signer.serial_number and candidate[1].issuer.public_bytes() == signed_data.signer.issuer:
            return candidate
    raise VerificationException(VerificationStatus.INVALID_CHAIN)

def _verify_signature(signed_data: _SignedData, signing_key: str):
    digest = _DIGESTS.get(signed_data.signer.digest_oid)
    if digest is None:
        raise ValueError('Unrecognized receipt digest algorithm ' + signed_data.signer.digest_oid)
    public_key = serialization.load_pem_public_key(signing_key.encode())
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise ValueError('Receipt signer key is not RSA')
    if signed_data.signer.signed_attributes is not None:
        signed_attributes = signed_data.signer.signed_attributes
        if not hmac.compare_digest(
            _message_digest_attribute(signed_attributes), hashlib.new(digest[0], signed_data.content).digest()
        ):
            raise ValueError('Receipt messageDigest attribute does not match the payload')
        # The signature covers the signed attributes re-encoded as an explicit SET (RFC 5652 5.4), so the
        # implicit [0] tag is swapped for a SET tag
        signed_bytes = b'\x31' + signed_attributes[1:]
    else:
        signed_bytes = signed_data.content
    public_key.verify(signed_data.signer.signature, signed_bytes, padding.PKCS1v15(), digest[1]())

def _message_digest_attribute(signed_attributes: bytes) -> bytes:
    for attribute in _children(signed_attributes, _read_element(signed_attributes, 0)):
        fields = _children(signed_attributes, _expect(signed_attributes, attribute, 0x30, 'Signed attribute'))
        if len(fields) == 2 and _decode_oid(signed_attributes, _expect(signed_attributes, fields[0], 0x06, 'Signed attribute')) == MESSAGE_DIGEST_OID:
            values = _children(signed_attributes, _expect(signed_attributes, fields[1], 0x31, 'Signed attribute'))
            if len(values) != 1:
                raise ValueError('Malformed messageDigest attribute')
            return _octets(signed_attributes, values[0], 'messageDigest attribute')
    raise ValueError('Receipt has no messageDigest attribute')

def _parse_attribute_set(der: bytes, what: str) -> List[Tuple[int, bytes]]:
    """
    Parses a receipt attribute SET, the shape both the receipt payload and the value of an in-app purchase
    attribute take. Each attribute is SEQUENCE { type INTEGER, version INTEGER, value OCTET STRING }.
    """
    element = _read_element(der, 0)
    if element.tag & ~0x20 == 0x04 and element.end == len(der):
        # Xcode receipts double-wrap the payload in an extra OCTET STRING; ReceiptUtility handles the same shape
        der = _octets(der, element, what)
        element = _read_element(der, 0)
    if element.tag != 0x31 or element.end != len(der):
        raise ValueError(what + ' is not an ASN.1 SET')
    attributes = []
    for attribute in _children(der, element):
        fields = _children(der, _expect(der, attribute, 0x30, 'Receipt attribute'))
        if len(fields) < 3:
            raise ValueError('Receipt attribute has fewer than 3 fields')
        attribute_type = _decode_bounded_integer(der, _expect(der, fields[0], 0x02, 'Receipt attribute type'))
        attributes.append((attribute_type, _octets(der, fields[2], 'Receipt attribute value')))
    return attributes

def _decode_bounded_integer(data: bytes, element: _Element) -> int:
    """Non-negative and within 64-bit range; real receipts carry 7-byte integers."""
    body = _content(data, element)
    if not body or len(body) > 8 or body[0] & 0x80:
        raise ValueError('Receipt integer out of range')
    return int.from_bytes(body, 'big')

def _decode_string(value: bytes) -> str:
    element = _read_element(value, 0)
    if element.tag not in (0x0C, 0x16) or element.end != len(value):
        raise ValueError('Attribute value is not an ASN.1 string')
    return _content(value, element).decode('utf-8')

def _decode_integer(value: bytes) -> int:
    element = _read_element(value, 0)
    if element.tag != 0x02 or element.end != len(value):
        raise ValueError('Attribute value is not an ASN.1 integer')
    return _decode_bounded_integer(value, element)

def _decode_date(value: bytes) -> Optional[int]:
    """RFC 3339 date in an IA5String, in milliseconds; empty means absent (real receipts do this)."""
    text = _decode_string(value)
    if text == '':
        return None
    parsed = datetime.datetime.fromisoformat(text.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Receipt date has no UTC offset: ' + text)
    return round(parsed.timestamp() * 1000)

def _record_unknown(unknown_attributes: Dict[int, List[bytes]], attribute_type: int, value: bytes):
    unknown_attributes.setdefault(attribute_type, []).append(value)

def _parse_receipt_payload(payload: bytes) -> AppReceipt:
    receipt = AppReceipt(inAppPurchases=[], unknownAttributes={})
    for attribute_type, value in _parse_attribute_set(payload, 'Receipt payload'):
        if attribute_type == ATTR_RECEIPT_TYPE:
            receipt.receiptType = _decode_string(value)
        elif attribute_type == ATTR_BUNDLE_ID:
            receipt.bundleId = _decode_string(value)
            receipt.bundleIdBytes = value
        elif attribute_type == ATTR_APP_VERSION:
            receipt.applicationVersion = _decode_string(value)
        elif attribute_type == ATTR_OPAQUE_VALUE:
            receipt.opaqueValue = value
        elif attribute_type == ATTR_SHA1_HASH:
            receipt.sha1Hash = value
        elif attribute_type == ATTR_CREATION_DATE:
            receipt.receiptCreationDate = _decode_date(value)
        elif attribute_type == ATTR_IN_APP:
            receipt.inAppPurchases.append(_parse_in_app_purchase(value))
        elif attribute_type == ATTR_ORIGINAL_PURCHASE_DATE:
            receipt.originalPurchaseDate = _decode_date(value)
        elif attribute_type == ATTR_ORIGINAL_APP_VERSION:
            receipt.originalApplicationVersion = _decode_string(value)
        elif attribute_type == ATTR_EXPIRATION_DATE:
            receipt.expirationDate = _decode_date(value)
        else:
            _record_unknown(receipt.unknownAttributes, attribute_type, value)
    return receipt

def _parse_in_app_purchase(in_app_set: bytes) -> InAppPurchaseReceipt:
    purchase = InAppPurchaseReceipt(unknownAttributes={})
    for attribute_type, value in _parse_attribute_set(in_app_set, 'In-app purchase attribute'):
        if attribute_type == IAP_QUANTITY:
            purchase.quantity = _decode_integer(value)
        elif attribute_type == IAP_PRODUCT_ID:
            purchase.productId = _decode_string(value)
        elif attribute_type == IAP_TRANSACTION_ID:
            purchase.transactionId = _decode_string(value)
        elif attribute_type == IAP_PURCHASE_DATE:
            purchase.purchaseDate = _decode_date(value)
        elif attribute_type == IAP_ORIGINAL_TRANSACTION_ID:
            purchase.originalTransactionId = _decode_string(value)
        elif attribute_type == IAP_ORIGINAL_PURCHASE_DATE:
            purchase.originalPurchaseDate = _decode_date(value)
        elif attribute_type == IAP_EXPIRES_DATE:
            purchase.expiresDate = _decode_date(value)
        elif attribute_type == IAP_WEB_ORDER_LINE_ITEM_ID:
            purchase.webOrderLineItemId = _decode_integer(value)
        elif attribute_type == IAP_CANCELLATION_DATE:
            purchase.cancellationDate = _decode_date(value)
        elif attribute_type == IAP_IS_IN_INTRO_OFFER_PERIOD:
            purchase.isInIntroOfferPeriod = _decode_integer(value) != 0
        else:
            _record_unknown(purchase.unknownAttributes, attribute_type, value)
    return purchase
