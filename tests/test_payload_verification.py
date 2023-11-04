# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
from base64 import b64decode
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.NotificationHistoryRequest import NotificationTypeV2

from appstoreserverlibrary.signed_data_verifier import VerificationException, VerificationStatus, SignedDataVerifier

from tests.util import get_signed_data_verifier, read_data_from_file

class PayloadVerification(unittest.TestCase):
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
        notification = verifier.verify_and_decode_signed_transaction(transaction_info)
        self.assertEqual(notification.environment, Environment.SANDBOX)

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
