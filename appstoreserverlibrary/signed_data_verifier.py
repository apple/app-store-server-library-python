# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import List, Optional
from base64 import b64decode
from enum import IntEnum
import time
import datetime

import asn1
import jwt
import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import SHA1, SHA256
from cryptography.x509 import ocsp, oid
from OpenSSL import crypto

from appstoreserverlibrary.models.AppTransaction import AppTransaction
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter

from .models.Environment import Environment
from .models.ResponseBodyV2DecodedPayload import ResponseBodyV2DecodedPayload
from .models.JWSTransactionDecodedPayload import JWSTransactionDecodedPayload
from .models.JWSRenewalInfoDecodedPayload import JWSRenewalInfoDecodedPayload

class SignedDataVerifier:
    """
    A class providing utility methods for verifying and decoding App Store signed data.
    """
    def __init__(
        self,
        root_certificates: List[bytes],
        enable_online_checks: bool,
        environment: Environment,
        bundle_id: str,
        app_apple_id: Optional[int] = None,
    ):
        self._chain_verifier = _ChainVerifier(root_certificates)
        self._environment = environment
        self._bundle_id = bundle_id
        self._app_apple_id = app_apple_id
        self._enable_online_checks = enable_online_checks
        if environment == Environment.PRODUCTION and app_apple_id is None:
            raise ValueError("appAppleId is required when the environment is Production")

    def verify_and_decode_renewal_info(self, signed_renewal_info: str) -> JWSRenewalInfoDecodedPayload:
        """
        Verifies and decodes a signedRenewalInfo obtained from the App Store Server API, an App Store Server Notification, or from a device
        See https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo

        :param signed_renewal_info: The signedRenewalInfo field
        :return: The decoded renewal info after verification
        :throws VerificationException: Thrown if the data could not be verified
        """
        
        decoded_renewal_info = _get_cattrs_converter(JWSRenewalInfoDecodedPayload).structure(self._decode_signed_object(signed_renewal_info), JWSRenewalInfoDecodedPayload)
        if decoded_renewal_info.environment != self._environment:
            raise VerificationException(VerificationStatus.INVALID_ENVIRONMENT)
        return decoded_renewal_info

    def verify_and_decode_signed_transaction(self, signed_transaction: str) -> JWSTransactionDecodedPayload:
        """
        Verifies and decodes a signedTransaction obtained from the App Store Server API, an App Store Server Notification, or from a device
        See https://developer.apple.com/documentation/appstoreserverapi/jwstransaction

        :param signed_transaction: The signedTransaction field
        :return: The decoded transaction info after verification
        :throws VerificationException: Thrown if the data could not be verified
        """
        decoded_transaction_info = _get_cattrs_converter(JWSTransactionDecodedPayload).structure(self._decode_signed_object(signed_transaction), JWSTransactionDecodedPayload)
        if decoded_transaction_info.bundleId != self._bundle_id:
            raise VerificationException(VerificationStatus.INVALID_APP_IDENTIFIER)
        if decoded_transaction_info.environment != self._environment:
            raise VerificationException(VerificationStatus.INVALID_ENVIRONMENT)
        return decoded_transaction_info

    def verify_and_decode_notification(self, signed_payload: str) -> ResponseBodyV2DecodedPayload:
        """
        Verifies and decodes an App Store Server Notification signedPayload
        See https://developer.apple.com/documentation/appstoreservernotifications/signedpayload

        :param signedPayload: The payload received by your server
        :return: The decoded payload after verification
        :throws VerificationException: Thrown if the data could not be verified
        """
        decoded_dict = self._decode_signed_object(signed_payload)
        decoded_signed_notification = _get_cattrs_converter(ResponseBodyV2DecodedPayload).structure(decoded_dict, ResponseBodyV2DecodedPayload)
        bundle_id = None
        app_apple_id = None
        environment = None
        if decoded_signed_notification.data:
            bundle_id = decoded_signed_notification.data.bundleId
            app_apple_id = decoded_signed_notification.data.appAppleId
            environment = decoded_signed_notification.data.environment
        elif decoded_signed_notification.summary:
            bundle_id = decoded_signed_notification.summary.bundleId
            app_apple_id = decoded_signed_notification.summary.appAppleId
            environment = decoded_signed_notification.summary.environment
        elif decoded_signed_notification.externalPurchaseToken:
            bundle_id = decoded_signed_notification.externalPurchaseToken.bundleId
            app_apple_id = decoded_signed_notification.externalPurchaseToken.appAppleId
            if decoded_signed_notification.externalPurchaseToken.externalPurchaseId and decoded_signed_notification.externalPurchaseToken.externalPurchaseId.startswith("SANDBOX"):
                environment = Environment.SANDBOX
            else:
                environment = Environment.PRODUCTION
        self._verify_notification(bundle_id, app_apple_id, environment)
        return decoded_signed_notification

    def _verify_notification(self, bundle_id: Optional[str], app_apple_id: Optional[int], environment: Optional[Environment]):
        if bundle_id != self._bundle_id or (self._environment == Environment.PRODUCTION and app_apple_id != self._app_apple_id):
            raise VerificationException(VerificationStatus.INVALID_APP_IDENTIFIER)
        if environment != self._environment:
            raise VerificationException(VerificationStatus.INVALID_ENVIRONMENT)

    def verify_and_decode_app_transaction(self, signed_app_transaction: str) -> AppTransaction:
        """
        Verifies and decodes a signed AppTransaction
        See https://developer.apple.com/documentation/storekit/apptransaction

        :param signed_app_transaction: The signed AppTransaction
        :return: The decoded AppTransaction after validation
        :throws VerificationException: Thrown if the data could not be verified
        """
        decoded_dict = self._decode_signed_object(signed_app_transaction)
        decoded_app_transaction = _get_cattrs_converter(AppTransaction).structure(decoded_dict, AppTransaction)
        environment = decoded_app_transaction.receiptType
        if decoded_app_transaction.bundleId != self._bundle_id or (self._environment == Environment.PRODUCTION and decoded_app_transaction.appAppleId != self._app_apple_id):
            raise VerificationException(VerificationStatus.INVALID_APP_IDENTIFIER)
        if environment != self._environment:
            raise VerificationException(VerificationStatus.INVALID_ENVIRONMENT)
        return decoded_app_transaction

    def _decode_signed_object(self, signed_obj: str) -> dict:
        try:
            decoded_jwt = jwt.decode(signed_obj, options={"verify_signature": False})
            if self._environment == Environment.XCODE or self._environment == Environment.LOCAL_TESTING:
                # Data is not signed by the App Store, and verification should be skipped
                # The environment MUST be checked in the public method calling this
                return decoded_jwt
            unverified_headers: dict = jwt.get_unverified_header(signed_obj)
            x5c_header: List[str] = unverified_headers.get("x5c")
            if x5c_header is None or len(x5c_header) == 0:
                raise Exception("x5c claim was empty")
            algorithm_header: str = unverified_headers.get("alg")
            if algorithm_header is None or "ES256" != algorithm_header:
                raise Exception("Algorithm was not ES256")
            signed_date = decoded_jwt.get('signedDate') if decoded_jwt.get('signedDate') is not None else decoded_jwt.get('receiptCreationDate')
            effective_date = time.time() if self._enable_online_checks or signed_date is None else int(signed_date) // 1000
            signing_key = self._chain_verifier.verify_chain(x5c_header, self._enable_online_checks, effective_date)
            return jwt.decode(signed_obj, signing_key, algorithms=["ES256"])
        except VerificationException as e:
            raise e
        except Exception as e:
            raise VerificationException(VerificationStatus.VERIFICATION_FAILURE) from e

class _ChainVerifier:
    def __init__(self, root_certificates: List[bytes], enable_strict_checks=True):
        self.enable_strict_checks = enable_strict_checks
        self.root_certificates = root_certificates

    def verify_chain(self, certificates: List[str], perform_online_checks: bool, effective_date: int) -> str:
        if len(self.root_certificates) == 0:
            raise VerificationException(VerificationStatus.INVALID_CERTIFICATE)
        if len(certificates) != 3:
            raise VerificationException(VerificationStatus.INVALID_CHAIN_LENGTH)
        trusted_store = crypto.X509Store()
        try:
            for trusted_cert_bytes in self.root_certificates:
                trusted_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, trusted_cert_bytes)
                trusted_store.add_cert(trusted_cert)
            if self.enable_strict_checks:
                trusted_store.set_flags(crypto.X509StoreFlags.X509_STRICT)
            leaf_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, b64decode(certificates[0], validate=True))
            intermediate_cert = crypto.load_certificate(crypto.FILETYPE_ASN1, b64decode(certificates[1], validate=True))
            verification_context = crypto.X509StoreContext(trusted_store, leaf_cert, [intermediate_cert])
        except Exception as e:
            raise VerificationException(VerificationStatus.INVALID_CERTIFICATE) from e

        trusted_store.set_time(datetime.datetime.fromtimestamp(effective_date, tz=datetime.timezone.utc))
        try:
            verification_context.verify_certificate()
            trusted_chain = verification_context.get_verified_chain()
        except Exception as e:
            raise VerificationException(VerificationStatus.VERIFICATION_FAILURE) from e
        self.check_oid(trusted_chain[0].to_cryptography(), "1.2.840.113635.100.6.11.1")
        self.check_oid(trusted_chain[1].to_cryptography(), "1.2.840.113635.100.6.2.1")
        if perform_online_checks:
            self.check_ocsp_status(trusted_chain[1], trusted_chain[2], trusted_chain[2])
            self.check_ocsp_status(trusted_chain[0], trusted_chain[1], trusted_chain[2])
        return (
            leaf_cert.to_cryptography()
            .public_key()
            .public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
            .decode()
        )

    def check_oid(self, cert: x509.Certificate, oid: str):
        try:
            cert.extensions.get_extension_for_oid(x509.ObjectIdentifier(oid))
        except Exception as e:
            raise VerificationException(VerificationStatus.VERIFICATION_FAILURE) from e

    def check_ocsp_status(self, cert: crypto.X509, issuer: crypto.X509, root: crypto.X509):
        builder = ocsp.OCSPRequestBuilder()
        builder = builder.add_certificate(cert.to_cryptography(), issuer.to_cryptography(), SHA256())
        req = builder.build()
        authority_values = (
            cert.to_cryptography()
            .extensions.get_extension_for_oid(x509.oid.ExtensionOID.AUTHORITY_INFORMATION_ACCESS)
            .value
        )
        ocsps = [val for val in authority_values if val.access_method == x509.oid.AuthorityInformationAccessOID.OCSP]
        for o in ocsps:
            r = requests.post(
                o.access_location.value,
                headers={"Content-Type": "application/ocsp-request"},
                data=req.public_bytes(serialization.Encoding.DER),
            )
            if r.status_code == 200:
                ocsp_resp = ocsp.load_der_ocsp_response(r.content)
                if ocsp_resp.response_status == ocsp.OCSPResponseStatus.SUCCESSFUL:
                    certs = [issuer]
                    for ocsp_cert in ocsp_resp.certificates:
                        certs.append(crypto.X509.from_cryptography(ocsp_cert))
                    # Find signing cert
                    signing_cert = None
                    for potential_signing_cert in certs:
                        if ocsp_resp.responder_key_hash:
                            subject_public_key_info = (
                                potential_signing_cert.get_pubkey()
                                .to_cryptography_key()
                                .public_bytes(
                                    encoding=serialization.Encoding.DER,
                                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                                )
                            )
                            decoder = asn1.Decoder()
                            decoder.start(subject_public_key_info)
                            decoder.enter()
                            decoder.read()
                            _, value = decoder.read()
                            digest = hashes.Hash(SHA1())
                            digest.update(value)
                            if digest.finalize() == ocsp_resp.responder_key_hash:
                                signing_cert = potential_signing_cert
                                break

                        elif ocsp_resp.responder_name:
                            if ocsp_resp.responder_name == potential_signing_cert.subject.rfc4514_string():
                                signing_cert = potential_signing_cert
                                break
                    if signing_cert is None:
                        raise VerificationException(VerificationStatus.VERIFICATION_FAILURE)

                    if signing_cert.to_cryptography().public_bytes(
                        encoding=serialization.Encoding.DER
                    ) == issuer.to_cryptography().public_bytes(encoding=serialization.Encoding.DER):
                        # We trust this because it is the issuer
                        pass
                    else:
                        trusted_store = crypto.X509Store()
                        trusted_store.add_cert(issuer)
                        trusted_store.add_cert(root)  # Apparently a full chain is always needed
                        verification_context = crypto.X509StoreContext(trusted_store, signing_cert, [])
                        verification_context.verify_certificate()
                        if (
                            oid.ExtendedKeyUsageOID.OCSP_SIGNING
                            not in signing_cert.to_cryptography()
                            .extensions.get_extension_for_class(x509.ExtendedKeyUsage)
                            .value._usages
                        ):
                            raise VerificationException(VerificationStatus.VERIFICATION_FAILURE)

                    # Confirm response is signed by signing_certificate
                    signing_cert.to_cryptography().public_key().verify(
                        ocsp_resp.signature, ocsp_resp.tbs_response_bytes, ECDSA(ocsp_resp.signature_hash_algorithm)
                    )

                    # Get the CertId
                    for single_response in ocsp_resp.responses:
                        # Get the cert ID with the provided hashing algorithm (using the request builder wrapper)
                        builder = ocsp.OCSPRequestBuilder()
                        builder = builder.add_certificate(
                            cert.to_cryptography(), issuer.to_cryptography(), single_response.hash_algorithm
                        )
                        req = builder.build()
                        if (
                            single_response.certificate_status == ocsp.OCSPCertStatus.GOOD
                            and single_response.serial_number == req.serial_number
                            and single_response.issuer_key_hash == req.issuer_key_hash
                            and single_response.issuer_name_hash == req.issuer_name_hash
                        ):
                            # Success
                            return

        raise VerificationException(VerificationStatus.VERIFICATION_FAILURE)


class VerificationStatus(IntEnum):
    OK = 0
    VERIFICATION_FAILURE = 1
    INVALID_APP_IDENTIFIER = 2
    INVALID_CERTIFICATE = 3
    INVALID_CHAIN_LENGTH = 4
    INVALID_CHAIN = 5
    INVALID_ENVIRONMENT = 6


class VerificationException(Exception):
    def __init__(self, status: VerificationStatus):
        super().__init__("Verification failed with status " + status.name)
        self.status = status
