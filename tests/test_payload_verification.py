# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Any, Dict
import unittest
from base64 import b64decode
from unittest.mock import MagicMock

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.NotificationHistoryRequest import NotificationTypeV2

from appstoreserverlibrary.signed_data_verifier import VerificationException, VerificationStatus, SignedDataVerifier

from tests.util import get_signed_data_verifier, read_data_from_binary_file, read_data_from_file

def sign_with_mocked_chain(verifier: SignedDataVerifier, payload: Dict[str, Any]) -> str:
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    verifier._chain_verifier.verify_chain = MagicMock(return_value=public_key)
    return jwt.encode(payload, private_key, algorithm='ES256', headers={'x5c': ['leaf', 'intermediate', 'root']})

def sign_without_chain(payload: Dict[str, Any]) -> str:
    private_key = ec.generate_private_key(ec.SECP256R1())
    return jwt.encode(payload, private_key, algorithm='ES256')

class PayloadVerification(unittest.TestCase):
    def test_production_environment_requires_app_apple_id(self):
        with self.assertRaises(ValueError):
            SignedDataVerifier([read_data_from_binary_file('tests/resources/certs/testCA.der')], False, Environment.PRODUCTION, "com.example", None)

    def test_app_store_server_notification_decoding(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        test_notification = read_data_from_file('tests/resources/mock_signed_data/testNotification')
        notification = verifier.verify_and_decode_notification(test_notification)
        self.assertEqual(notification.notificationType, NotificationTypeV2.TEST)

    def test_app_store_server_notification_decoding_production(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example")
        test_notification = read_data_from_file('tests/resources/mock_signed_data/testNotification')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(test_notification)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

    def test_missing_x5c_header(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        missing_x5c_header_claim = read_data_from_file('tests/resources/mock_signed_data/missingX5CHeaderClaim')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(missing_x5c_header_claim)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_wrong_bundle_id_for_server_notification(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.examplex")
        wrong_bundle = read_data_from_file('tests/resources/mock_signed_data/wrongBundleId')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(wrong_bundle)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_wrong_app_apple_id_for_server_notification(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1235)
        test_notification = read_data_from_file('tests/resources/mock_signed_data/testNotification')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(test_notification)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_renewal_info_decoding(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        renewal_info = read_data_from_file('tests/resources/mock_signed_data/renewalInfo')
        notification = verifier.verify_and_decode_renewal_info(renewal_info)
        self.assertEqual(notification.environment, Environment.SANDBOX)

    def test_transaction_info_decoding(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        transaction_info = read_data_from_file('tests/resources/mock_signed_data/transactionInfo')
        notification = verifier.verify_and_decode_transaction(transaction_info)
        self.assertEqual(notification.environment, Environment.SANDBOX)

    def test_wrong_bundle_id_for_transaction(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.examplex")
        transaction_info = read_data_from_file('tests/resources/mock_signed_data/transactionInfo')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_transaction(transaction_info)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_wrong_environment_for_transaction(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example")
        transaction_info = read_data_from_file('tests/resources/mock_signed_data/transactionInfo')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_transaction(transaction_info)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

    def test_wrong_environment_for_renewal_info(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example")
        renewal_info = read_data_from_file('tests/resources/mock_signed_data/renewalInfo')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_renewal_info(renewal_info)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

    def test_app_transaction_decoding_production(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_app_transaction = sign_with_mocked_chain(verifier, {"receiptType": "Production", "appAppleId": 1234, "bundleId": "com.example", "receiptCreationDate": 1698148900000})
        app_transaction = verifier.verify_and_decode_app_transaction(signed_app_transaction)
        self.assertEqual(Environment.PRODUCTION, app_transaction.receiptType)
        self.assertEqual(1234, app_transaction.appAppleId)
        self.assertEqual(1, verifier._chain_verifier.verify_chain.call_count)

    def test_wrong_bundle_id_for_app_transaction(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_app_transaction = sign_with_mocked_chain(verifier, {"receiptType": "Production", "appAppleId": 1234, "bundleId": "com.examplex", "receiptCreationDate": 1698148900000})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_transaction(signed_app_transaction)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_wrong_app_apple_id_for_app_transaction(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_app_transaction = sign_with_mocked_chain(verifier, {"receiptType": "Production", "appAppleId": 1235, "bundleId": "com.example", "receiptCreationDate": 1698148900000})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_transaction(signed_app_transaction)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_wrong_environment_for_app_transaction(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_app_transaction = sign_with_mocked_chain(verifier, {"receiptType": "Sandbox", "appAppleId": 1234, "bundleId": "com.example", "receiptCreationDate": 1698148900000})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_transaction(signed_app_transaction)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

    def test_realtime_request_decoding_production(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_realtime_request = sign_with_mocked_chain(verifier, self._realtime_request(1234, "Production"))
        realtime_request = verifier.verify_and_decode_realtime_request(signed_realtime_request)
        self.assertEqual(Environment.PRODUCTION, realtime_request.environment)
        self.assertEqual(1234, realtime_request.appAppleId)

    def test_wrong_app_apple_id_for_realtime_request(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_realtime_request = sign_with_mocked_chain(verifier, self._realtime_request(1235, "Production"))
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_realtime_request(signed_realtime_request)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_wrong_environment_for_realtime_request(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1234)
        signed_realtime_request = sign_with_mocked_chain(verifier, self._realtime_request(1234, "Sandbox"))
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_realtime_request(signed_realtime_request)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

    def test_algorithm_other_than_es256(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        signed_transaction = jwt.encode({"bundleId": "com.example", "environment": "Sandbox", "signedDate": 1672956154000}, "a-shared-secret-of-at-least-thirty-two-bytes", algorithm='HS256', headers={'x5c': ['leaf', 'intermediate', 'root']})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_transaction(signed_transaction)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_transaction(self):
        verifier = get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example")
        signed_transaction = sign_without_chain({"bundleId": "com.example", "environment": "LocalTesting", "signedDate": "notanumber"})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_transaction(signed_transaction)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_renewal_info(self):
        verifier = get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example")
        signed_renewal_info = sign_without_chain({"environment": "LocalTesting", "signedDate": "notanumber"})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_renewal_info(signed_renewal_info)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_notification(self):
        verifier = get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example")
        signed_notification = sign_without_chain({"notificationType": "TEST", "signedDate": "notanumber"})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(signed_notification)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_app_transaction(self):
        verifier = get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example")
        signed_app_transaction = sign_without_chain({"receiptType": "LocalTesting", "bundleId": "com.example", "receiptCreationDate": "notanumber"})
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_transaction(signed_app_transaction)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_realtime_request(self):
        verifier = get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example")
        realtime_request = self._realtime_request(1234, "LocalTesting")
        realtime_request["signedDate"] = "notanumber"
        signed_realtime_request = sign_without_chain(realtime_request)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_realtime_request(signed_realtime_request)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def _realtime_request(self, app_apple_id: int, environment: str) -> Dict[str, Any]:
        return {
            "originalTransactionId": "99371282",
            "appAppleId": app_apple_id,
            "productId": "com.example.product",
            "userLocale": "en-US",
            "requestIdentifier": "3db5c98d-8acf-4e29-831e-8e1f82f9f6e9",
            "environment": environment,
            "signedDate": 1698148900000
        }

    def test_malformed_jwt_with_too_many_parts(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification("a.b.c.d")
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_jwt_with_malformed_data(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification("a.b.c")
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

if __name__ == '__main__':
    unittest.main()
