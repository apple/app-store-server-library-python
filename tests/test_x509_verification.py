# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import datetime
import time
import unittest
from typing import List, Optional
from unittest import mock
from unittest.mock import MagicMock, patch

import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509 import ocsp
from cryptography.x509.oid import AuthorityInformationAccessOID, ExtendedKeyUsageOID, NameOID

from appstoreserverlibrary.signed_data_verifier import _ChainVerifier, VerificationException, VerificationStatus
from base64 import b64decode, b64encode

ROOT_CA_BASE64_ENCODED = "MIIBgjCCASmgAwIBAgIJALUc5ALiH5pbMAoGCCqGSM49BAMDMDYxCzAJBgNVBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlDdXBlcnRpbm8wHhcNMjMwMTA1MjEzMDIyWhcNMzMwMTAyMjEzMDIyWjA2MQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJQ3VwZXJ0aW5vMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEc+/Bl+gospo6tf9Z7io5tdKdrlN1YdVnqEhEDXDShzdAJPQijamXIMHf8xWWTa1zgoYTxOKpbuJtDplz1XriTaMgMB4wDAYDVR0TBAUwAwEB/zAOBgNVHQ8BAf8EBAMCAQYwCgYIKoZIzj0EAwMDRwAwRAIgemWQXnMAdTad2JDJWng9U4uBBL5mA7WI05H7oH7c6iQCIHiRqMjNfzUAyiu9h6rOU/K+iTR0I/3Y/NSWsXHX+acc"
INTERMEDIATE_CA_BASE64_ENCODED = "MIIBnzCCAUWgAwIBAgIBCzAKBggqhkjOPQQDAzA2MQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJQ3VwZXJ0aW5vMB4XDTIzMDEwNTIxMzEwNVoXDTMzMDEwMTIxMzEwNVowRTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRIwEAYDVQQHDAlDdXBlcnRpbm8xFTATBgNVBAoMDEludGVybWVkaWF0ZTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABBUN5V9rKjfRiMAIojEA0Av5Mp0oF+O0cL4gzrTF178inUHugj7Et46NrkQ7hKgMVnjogq45Q1rMs+cMHVNILWqjNTAzMA8GA1UdEwQIMAYBAf8CAQAwDgYDVR0PAQH/BAQDAgEGMBAGCiqGSIb3Y2QGAgEEAgUAMAoGCCqGSM49BAMDA0gAMEUCIQCmsIKYs41ullssHX4rVveUT0Z7Is5/hLK1lFPTtun3hAIgc2+2RG5+gNcFVcs+XJeEl4GZ+ojl3ROOmll+ye7dynQ="
LEAF_CERT_BASE64_ENCODED = "MIIBoDCCAUagAwIBAgIBDDAKBggqhkjOPQQDAzBFMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExEjAQBgNVBAcMCUN1cGVydGlubzEVMBMGA1UECgwMSW50ZXJtZWRpYXRlMB4XDTIzMDEwNTIxMzEzNFoXDTMzMDEwMTIxMzEzNFowPTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRIwEAYDVQQHDAlDdXBlcnRpbm8xDTALBgNVBAoMBExlYWYwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATitYHEaYVuc8g9AjTOwErMvGyPykPa+puvTI8hJTHZZDLGas2qX1+ErxgQTJgVXv76nmLhhRJH+j25AiAI8iGsoy8wLTAJBgNVHRMEAjAAMA4GA1UdDwEB/wQEAwIHgDAQBgoqhkiG92NkBgsBBAIFADAKBggqhkjOPQQDAwNIADBFAiBX4c+T0Fp5nJ5QRClRfu5PSByRvNPtuaTsk0vPB3WAIAIhANgaauAj/YP9s0AkEhyJhxQO/6Q2zouZ+H1CIOehnMzQ"

INTERMEDIATE_CA_INVALID_OID_BASE64_ENCODED = "MIIBnjCCAUWgAwIBAgIBDTAKBggqhkjOPQQDAzA2MQswCQYDVQQGEwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJQ3VwZXJ0aW5vMB4XDTIzMDEwNTIxMzYxNFoXDTMzMDEwMTIxMzYxNFowRTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRIwEAYDVQQHDAlDdXBlcnRpbm8xFTATBgNVBAoMDEludGVybWVkaWF0ZTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABBUN5V9rKjfRiMAIojEA0Av5Mp0oF+O0cL4gzrTF178inUHugj7Et46NrkQ7hKgMVnjogq45Q1rMs+cMHVNILWqjNTAzMA8GA1UdEwQIMAYBAf8CAQAwDgYDVR0PAQH/BAQDAgEGMBAGCiqGSIb3Y2QGAgIEAgUAMAoGCCqGSM49BAMDA0cAMEQCIFROtTE+RQpKxNXETFsf7Mc0h+5IAsxxo/X6oCC/c33qAiAmC5rn5yCOOEjTY4R1H1QcQVh+eUwCl13NbQxWCuwxxA=="
LEAF_CERT_FOR_INTERMEDIATE_CA_INVALID_OID_BASE64_ENCODED = "MIIBnzCCAUagAwIBAgIBDjAKBggqhkjOPQQDAzBFMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExEjAQBgNVBAcMCUN1cGVydGlubzEVMBMGA1UECgwMSW50ZXJtZWRpYXRlMB4XDTIzMDEwNTIxMzY1OFoXDTMzMDEwMTIxMzY1OFowPTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRIwEAYDVQQHDAlDdXBlcnRpbm8xDTALBgNVBAoMBExlYWYwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATitYHEaYVuc8g9AjTOwErMvGyPykPa+puvTI8hJTHZZDLGas2qX1+ErxgQTJgVXv76nmLhhRJH+j25AiAI8iGsoy8wLTAJBgNVHRMEAjAAMA4GA1UdDwEB/wQEAwIHgDAQBgoqhkiG92NkBgsBBAIFADAKBggqhkjOPQQDAwNHADBEAiAUAs+gzYOsEXDwQquvHYbcVymyNqDtGw9BnUFp2YLuuAIgXxQ3Ie9YU0cMqkeaFd+lyo0asv9eyzk6stwjeIeOtTU="
LEAF_CERT_INVALID_OID_BASE64_ENCODED = "MIIBoDCCAUagAwIBAgIBDzAKBggqhkjOPQQDAzBFMQswCQYDVQQGEwJVUzELMAkGA1UECAwCQ0ExEjAQBgNVBAcMCUN1cGVydGlubzEVMBMGA1UECgwMSW50ZXJtZWRpYXRlMB4XDTIzMDEwNTIxMzczMVoXDTMzMDEwMTIxMzczMVowPTELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRIwEAYDVQQHDAlDdXBlcnRpbm8xDTALBgNVBAoMBExlYWYwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATitYHEaYVuc8g9AjTOwErMvGyPykPa+puvTI8hJTHZZDLGas2qX1+ErxgQTJgVXv76nmLhhRJH+j25AiAI8iGsoy8wLTAJBgNVHRMEAjAAMA4GA1UdDwEB/wQEAwIHgDAQBgoqhkiG92NkBgsCBAIFADAKBggqhkjOPQQDAwNIADBFAiAb+7S3i//bSGy7skJY9+D4VgcQLKFeYfIMSrUCmdrFqwIhAIMVwzD1RrxPRtJyiOCXLyibIvwcY+VS73HYfk0O9lgz"

LEAF_CERT_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE4rWBxGmFbnPIPQI0zsBKzLxsj8pD\n2vqbr0yPISUx2WQyxmrNql9fhK8YEEyYFV7++p5i4YUSR/o9uQIgCPIhrA==\n-----END PUBLIC KEY-----\n"

REAL_APPLE_ROOT_BASE64_ENCODED = "MIICQzCCAcmgAwIBAgIILcX8iNLFS5UwCgYIKoZIzj0EAwMwZzEbMBkGA1UEAwwSQXBwbGUgUm9vdCBDQSAtIEczMSYwJAYDVQQLDB1BcHBsZSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTETMBEGA1UECgwKQXBwbGUgSW5jLjELMAkGA1UEBhMCVVMwHhcNMTQwNDMwMTgxOTA2WhcNMzkwNDMwMTgxOTA2WjBnMRswGQYDVQQDDBJBcHBsZSBSb290IENBIC0gRzMxJjAkBgNVBAsMHUFwcGxlIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MRMwEQYDVQQKDApBcHBsZSBJbmMuMQswCQYDVQQGEwJVUzB2MBAGByqGSM49AgEGBSuBBAAiA2IABJjpLz1AcqTtkyJygRMc3RCV8cWjTnHcFBbZDuWmBSp3ZHtfTjjTuxxEtX/1H7YyYl3J6YRbTzBPEVoA/VhYDKX1DyxNB0cTddqXl5dvMVztK517IDvYuVTZXpmkOlEKMaNCMEAwHQYDVR0OBBYEFLuw3qFYM4iapIqZ3r6966/ayySrMA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0PAQH/BAQDAgEGMAoGCCqGSM49BAMDA2gAMGUCMQCD6cHEFl4aXTQY2e3v9GwOAEZLuN+yRhHFD/3meoyhpmvOwgPUnPWTxnS4at+qIxUCMG1mihDK1A3UT82NQz60imOlM27jbdoXt2QfyFMm+YhidDkLF1vLUagM6BgD56KyKA=="
REAL_APPLE_INTERMEDIATE_BASE64_ENCODED = "MIIDFjCCApygAwIBAgIUIsGhRwp0c2nvU4YSycafPTjzbNcwCgYIKoZIzj0EAwMwZzEbMBkGA1UEAwwSQXBwbGUgUm9vdCBDQSAtIEczMSYwJAYDVQQLDB1BcHBsZSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTETMBEGA1UECgwKQXBwbGUgSW5jLjELMAkGA1UEBhMCVVMwHhcNMjEwMzE3MjAzNzEwWhcNMzYwMzE5MDAwMDAwWjB1MUQwQgYDVQQDDDtBcHBsZSBXb3JsZHdpZGUgRGV2ZWxvcGVyIFJlbGF0aW9ucyBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTELMAkGA1UECwwCRzYxEzARBgNVBAoMCkFwcGxlIEluYy4xCzAJBgNVBAYTAlVTMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEbsQKC94PrlWmZXnXgtxzdVJL8T0SGYngDRGpngn3N6PT8JMEb7FDi4bBmPhCnZ3/sq6PF/cGcKXWsL5vOteRhyJ45x3ASP7cOB+aao90fcpxSv/EZFbniAbNgZGhIhpIo4H6MIH3MBIGA1UdEwEB/wQIMAYBAf8CAQAwHwYDVR0jBBgwFoAUu7DeoVgziJqkipnevr3rr9rLJKswRgYIKwYBBQUHAQEEOjA4MDYGCCsGAQUFBzABhipodHRwOi8vb2NzcC5hcHBsZS5jb20vb2NzcDAzLWFwcGxlcm9vdGNhZzMwNwYDVR0fBDAwLjAsoCqgKIYmaHR0cDovL2NybC5hcHBsZS5jb20vYXBwbGVyb290Y2FnMy5jcmwwHQYDVR0OBBYEFD8vlCNR01DJmig97bB85c+lkGKZMA4GA1UdDwEB/wQEAwIBBjAQBgoqhkiG92NkBgIBBAIFADAKBggqhkjOPQQDAwNoADBlAjBAXhSq5IyKogMCPtw490BaB677CaEGJXufQB/EqZGd6CSjiCtOnuMTbXVXmxxcxfkCMQDTSPxarZXvNrkxU3TkUMI33yzvFVVRT4wxWJC994OsdcZ4+RGNsYDyR5gmdr0nDGg="
REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED = "MIIEMTCCA7agAwIBAgIQR8KHzdn554Z/UoradNx9tzAKBggqhkjOPQQDAzB1MUQwQgYDVQQDDDtBcHBsZSBXb3JsZHdpZGUgRGV2ZWxvcGVyIFJlbGF0aW9ucyBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTELMAkGA1UECwwCRzYxEzARBgNVBAoMCkFwcGxlIEluYy4xCzAJBgNVBAYTAlVTMB4XDTI1MDkxOTE5NDQ1MVoXDTI3MTAxMzE3NDcyM1owgZIxQDA+BgNVBAMMN1Byb2QgRUNDIE1hYyBBcHAgU3RvcmUgYW5kIGlUdW5lcyBTdG9yZSBSZWNlaXB0IFNpZ25pbmcxLDAqBgNVBAsMI0FwcGxlIFdvcmxkd2lkZSBEZXZlbG9wZXIgUmVsYXRpb25zMRMwEQYDVQQKDApBcHBsZSBJbmMuMQswCQYDVQQGEwJVUzBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABNnVvhcv7iT+7Ex5tBMBgrQspHzIsXRi0Yxfek7lv8wEmj/bHiWtNwJqc2BoHzsQiEjP7KFIIKg4Y8y0/nynuAmjggIIMIICBDAMBgNVHRMBAf8EAjAAMB8GA1UdIwQYMBaAFD8vlCNR01DJmig97bB85c+lkGKZMHAGCCsGAQUFBwEBBGQwYjAtBggrBgEFBQcwAoYhaHR0cDovL2NlcnRzLmFwcGxlLmNvbS93d2RyZzYuZGVyMDEGCCsGAQUFBzABhiVodHRwOi8vb2NzcC5hcHBsZS5jb20vb2NzcDAzLXd3ZHJnNjAyMIIBHgYDVR0gBIIBFTCCAREwggENBgoqhkiG92NkBQYBMIH+MIHDBggrBgEFBQcCAjCBtgyBs1JlbGlhbmNlIG9uIHRoaXMgY2VydGlmaWNhdGUgYnkgYW55IHBhcnR5IGFzc3VtZXMgYWNjZXB0YW5jZSBvZiB0aGUgdGhlbiBhcHBsaWNhYmxlIHN0YW5kYXJkIHRlcm1zIGFuZCBjb25kaXRpb25zIG9mIHVzZSwgY2VydGlmaWNhdGUgcG9saWN5IGFuZCBjZXJ0aWZpY2F0aW9uIHByYWN0aWNlIHN0YXRlbWVudHMuMDYGCCsGAQUFBwIBFipodHRwOi8vd3d3LmFwcGxlLmNvbS9jZXJ0aWZpY2F0ZWF1dGhvcml0eS8wHQYDVR0OBBYEFIFioG4wMMVA1ku9zJmGNPAVn3eqMA4GA1UdDwEB/wQEAwIHgDAQBgoqhkiG92NkBgsBBAIFADAKBggqhkjOPQQDAwNpADBmAjEA+qXnREC7hXIWVLsLxznjRpIzPf7VHz9V/CTm8+LJlrQepnmcPvGLNcX6XPnlcgLAAjEA5IjNZKgg5pQ79knF4IbTXdKv8vutIDMXDmjPVT3dGvFtsGRwXOywR2kZCdSrfeot"

EFFECTIVE_DATE = 1761962975
CLOCK_DATE = 41231

def _create_certificate(subject: str, issuer: x509.Name, public_key, signing_key, is_ca: bool, extensions: List[x509.ExtensionType]) -> x509.Certificate:
    now = datetime.datetime.now(datetime.timezone.utc)
    builder = x509.CertificateBuilder() \
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject)])) \
        .issuer_name(issuer) \
        .public_key(public_key) \
        .serial_number(x509.random_serial_number()) \
        .not_valid_before(now - datetime.timedelta(days=1)) \
        .not_valid_after(now + datetime.timedelta(days=365)) \
        .add_extension(x509.BasicConstraints(ca=is_ca, path_length=None), critical=True)
    for extension in extensions:
        builder = builder.add_extension(extension, critical=False)
    return builder.sign(signing_key, hashes.SHA256())

def _ocsp_access(url: str) -> x509.AuthorityInformationAccess:
    return x509.AuthorityInformationAccess([x509.AccessDescription(AuthorityInformationAccessOID.OCSP, x509.UniformResourceIdentifier(url))])

class _GeneratedChain:
    def __init__(self):
        self.root_key = ec.generate_private_key(ec.SECP256R1())
        self.intermediate_key = ec.generate_private_key(ec.SECP256R1())
        self.leaf_key = ec.generate_private_key(ec.SECP256R1())
        root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Root")])
        self.root = _create_certificate("Root", root_name, self.root_key.public_key(), self.root_key, True, [])
        self.intermediate = _create_certificate("Intermediate", root_name, self.intermediate_key.public_key(), self.root_key, True, [
            x509.UnrecognizedExtension(x509.ObjectIdentifier("1.2.840.113635.100.6.2.1"), b"\x05\x00"),
            _ocsp_access("http://ocsp.example.com/root"),
        ])
        self.leaf = _create_certificate("Leaf", self.intermediate.subject, self.leaf_key.public_key(), self.intermediate_key, False, [
            x509.UnrecognizedExtension(x509.ObjectIdentifier("1.2.840.113635.100.6.11.1"), b"\x05\x00"),
            _ocsp_access("http://ocsp.example.com/intermediate"),
        ])

    def root_bytes(self) -> bytes:
        return self.root.public_bytes(serialization.Encoding.DER)

    def chain(self) -> List[str]:
        return [b64encode(cert.public_bytes(serialization.Encoding.DER)).decode() for cert in [self.leaf, self.intermediate, self.root]]

    def leaf_public_key(self) -> str:
        return self.leaf_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()

    def ocsp_responder(self, responder_encoding: ocsp.OCSPResponderEncoding = ocsp.OCSPResponderEncoding.HASH, delegated_signer_usages: Optional[List[x509.ObjectIdentifier]] = None, cert_status: ocsp.OCSPCertStatus = ocsp.OCSPCertStatus.GOOD):
        def post(url, headers, data, timeout):
            request = ocsp.load_der_ocsp_request(data)
            if request.serial_number == self.leaf.serial_number:
                cert, issuer, issuer_key = self.leaf, self.intermediate, self.intermediate_key
            else:
                cert, issuer, issuer_key = self.intermediate, self.root, self.root_key
            now = datetime.datetime.now(datetime.timezone.utc)
            builder = ocsp.OCSPResponseBuilder().add_response(
                cert=cert,
                issuer=issuer,
                algorithm=hashes.SHA256(),
                cert_status=cert_status,
                this_update=now - datetime.timedelta(minutes=1),
                next_update=now + datetime.timedelta(hours=1),
                revocation_time=now - datetime.timedelta(days=1) if cert_status == ocsp.OCSPCertStatus.REVOKED else None,
                revocation_reason=None
            )
            signing_cert, signing_key = issuer, issuer_key
            if delegated_signer_usages is not None:
                signing_key = ec.generate_private_key(ec.SECP256R1())
                signing_cert = _create_certificate("Delegated OCSP Signer", issuer.subject, signing_key.public_key(), issuer_key, False, [x509.ExtendedKeyUsage(delegated_signer_usages)])
                builder = builder.certificates([signing_cert])
            builder = builder.responder_id(responder_encoding, signing_cert)
            response = MagicMock()
            response.status_code = 200
            response.content = builder.sign(signing_key, hashes.SHA256()).public_bytes(serialization.Encoding.DER)
            return response
        return post

class X509Verification(unittest.TestCase):
    def test_valid_chain_without_ocsp(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)], False)
        public_key = verifier.verify_chain([
            LEAF_CERT_BASE64_ENCODED,
            INTERMEDIATE_CA_BASE64_ENCODED,
            ROOT_CA_BASE64_ENCODED
        ], False, EFFECTIVE_DATE)
        self.assertEqual(LEAF_CERT_PUBLIC_KEY, public_key)

    def test_valid_chain_invalid_intermediate_OID_without_OCSP(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)], False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([
                LEAF_CERT_FOR_INTERMEDIATE_CA_INVALID_OID_BASE64_ENCODED,
                INTERMEDIATE_CA_INVALID_OID_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_valid_chain_invalid_leaf_OID_without_OCSP(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)], False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([
                LEAF_CERT_INVALID_OID_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_invalid_chain_length(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)], False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([INTERMEDIATE_CA_BASE64_ENCODED, ROOT_CA_BASE64_ENCODED], False, EFFECTIVE_DATE)
        self.assertIn('Verification failed with status INVALID_CHAIN_LENGTH', str(context.exception))

    def test_invalid_base64_in_certificate_list(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)])
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([
                "abc",
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.INVALID_CERTIFICATE, context.exception.status)

    def test_invalid_data_in_certificate_list(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)], False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([
                str(b64encode(b"abc")),
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.INVALID_CERTIFICATE, context.exception.status)
    def test_malformed_root_cert(self):
        verifier = _ChainVerifier([b64decode(b64encode(b"abc"))])
        with self.assertRaises(Exception) as context:
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.INVALID_CERTIFICATE, context.exception.status)

    def test_chain_different_than_root_certificate(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)], False)

        with self.assertRaises(Exception) as context:
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_valid_expired_chain(self):
        verifier = _ChainVerifier([b64decode(ROOT_CA_BASE64_ENCODED)], False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, 2280946846)
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_apple_chain_is_valid_with_ocsp_and_strict(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)])
        verifier.verify_chain([
            REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED,
            REAL_APPLE_INTERMEDIATE_BASE64_ENCODED,
            REAL_APPLE_ROOT_BASE64_ENCODED
        ], True, EFFECTIVE_DATE)

    def test_ocsp_response_caching(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)])
        magic_mock = MagicMock(return_value=LEAF_CERT_BASE64_ENCODED)
        verifier._verify_chain_without_caching = magic_mock
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)):
            verifier.verify_chain([
                REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED,
                REAL_APPLE_INTERMEDIATE_BASE64_ENCODED,
                REAL_APPLE_ROOT_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(1, magic_mock.call_count)
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE + 1)): # 1 second
            verifier.verify_chain([
                REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED,
                REAL_APPLE_INTERMEDIATE_BASE64_ENCODED,
                REAL_APPLE_ROOT_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(1, magic_mock.call_count)

    def test_ocsp_response_caching_has_expiration(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)])
        magic_mock = MagicMock(return_value=LEAF_CERT_BASE64_ENCODED)
        verifier._verify_chain_without_caching = magic_mock
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)):
            verifier.verify_chain([
                REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED,
                REAL_APPLE_INTERMEDIATE_BASE64_ENCODED,
                REAL_APPLE_ROOT_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(1, magic_mock.call_count)
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE + 900)): # 15 minutes
            verifier.verify_chain([
                REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED,
                REAL_APPLE_INTERMEDIATE_BASE64_ENCODED,
                REAL_APPLE_ROOT_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(2, magic_mock.call_count)

    def test_ocsp_response_caching_with_different_chain(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)])
        magic_mock = MagicMock(return_value=LEAF_CERT_BASE64_ENCODED)
        verifier._verify_chain_without_caching = magic_mock
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)):
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(1, magic_mock.call_count)
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)): # Same
            verifier.verify_chain([
                REAL_APPLE_SIGNING_CERTIFICATE_BASE64_ENCODED,
                REAL_APPLE_INTERMEDIATE_BASE64_ENCODED,
                REAL_APPLE_ROOT_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(2, magic_mock.call_count)

    def test_ocsp_response_caching_with_slightly_different_chain(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)])
        magic_mock = MagicMock(return_value=LEAF_CERT_BASE64_ENCODED)
        verifier._verify_chain_without_caching = magic_mock
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)):
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(1, magic_mock.call_count)
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)): # Same
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                REAL_APPLE_ROOT_BASE64_ENCODED
            ], True, EFFECTIVE_DATE)
        self.assertEqual(2, magic_mock.call_count)

    def test_ocsp_response_caching_evicts_expired_entries(self):
        verifier = _ChainVerifier([b64decode(REAL_APPLE_ROOT_BASE64_ENCODED)])
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE)):
            for i in range(_ChainVerifier.MAXIMUM_CACHE_SIZE):
                verifier.put_verified_public_key(["leaf" + str(i), "intermediate", "root"], "key" + str(i))
        self.assertEqual(_ChainVerifier.MAXIMUM_CACHE_SIZE, len(verifier.verified_certificates_cache))
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE + 1)):
            verifier.put_verified_public_key(["leaf", "intermediate", "root"], "key")
        self.assertEqual(_ChainVerifier.MAXIMUM_CACHE_SIZE + 1, len(verifier.verified_certificates_cache))
        with patch('time.time', mock.MagicMock(return_value=CLOCK_DATE + 900)):
            verifier.put_verified_public_key(["newLeaf", "intermediate", "root"], "newKey")
            self.assertEqual(2, len(verifier.verified_certificates_cache))
            self.assertEqual("key", verifier.get_cached_public_key(["leaf", "intermediate", "root"]))
            self.assertEqual("newKey", verifier.get_cached_public_key(["newLeaf", "intermediate", "root"]))
            self.assertIsNone(verifier.get_cached_public_key(["leaf0", "intermediate", "root"]))

    def test_empty_root_certificates(self):
        verifier = _ChainVerifier([], False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_chain([
                LEAF_CERT_BASE64_ENCODED,
                INTERMEDIATE_CA_BASE64_ENCODED,
                ROOT_CA_BASE64_ENCODED
            ], False, EFFECTIVE_DATE)
        self.assertEqual(VerificationStatus.INVALID_CERTIFICATE, context.exception.status)

    def test_ocsp_responder_identified_by_key_hash(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=chain.ocsp_responder(responder_encoding=ocsp.OCSPResponderEncoding.HASH)) as post:
            public_key = verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(chain.leaf_public_key(), public_key)
        self.assertEqual(2, post.call_count)

    def test_ocsp_responder_identified_by_name(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=chain.ocsp_responder(responder_encoding=ocsp.OCSPResponderEncoding.NAME)) as post:
            public_key = verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(chain.leaf_public_key(), public_key)
        self.assertEqual(2, post.call_count)

    def test_ocsp_delegated_signer_identified_by_key_hash(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=chain.ocsp_responder(responder_encoding=ocsp.OCSPResponderEncoding.HASH, delegated_signer_usages=[ExtendedKeyUsageOID.OCSP_SIGNING])):
            public_key = verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(chain.leaf_public_key(), public_key)

    def test_ocsp_delegated_signer_identified_by_name(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=chain.ocsp_responder(responder_encoding=ocsp.OCSPResponderEncoding.NAME, delegated_signer_usages=[ExtendedKeyUsageOID.OCSP_SIGNING])):
            public_key = verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(chain.leaf_public_key(), public_key)

    def test_ocsp_delegated_signer_without_ocsp_signing_usage(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=chain.ocsp_responder(delegated_signer_usages=[ExtendedKeyUsageOID.SERVER_AUTH])):
            with self.assertRaises(VerificationException) as context:
                verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_ocsp_revoked_certificate(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=chain.ocsp_responder(cert_status=ocsp.OCSPCertStatus.REVOKED)):
            with self.assertRaises(VerificationException) as context:
                verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_ocsp_network_failure_is_retryable(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        with patch('requests.post', side_effect=requests.exceptions.ConnectionError()):
            with self.assertRaises(VerificationException) as context:
                verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(VerificationStatus.RETRYABLE_VERIFICATION_FAILURE, context.exception.status)

    def test_ocsp_unsuccessful_http_status_is_retryable(self):
        chain = _GeneratedChain()
        verifier = _ChainVerifier([chain.root_bytes()], False)
        response = MagicMock()
        response.status_code = 503
        with patch('requests.post', return_value=response):
            with self.assertRaises(VerificationException) as context:
                verifier.verify_chain(chain.chain(), True, time.time())
        self.assertEqual(VerificationStatus.RETRYABLE_VERIFICATION_FAILURE, context.exception.status)


if __name__ == '__main__':
    unittest.main()
