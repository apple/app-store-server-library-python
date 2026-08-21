# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import datetime
import unittest
from base64 import b64encode

from appstoreserverlibrary.app_receipt_verifier import AppReceiptVerifier
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.signed_data_verifier import VerificationException, VerificationStatus

from tests.receipt_creator import AttributeSet, ReceiptCreator, create_receipt_creator, create_self_signed_receipt_creator, days_ago, double_wrap, encode, in_one_year
from tests.util import read_data_from_binary_file, read_data_from_file

XCODE_BUNDLE_ID = "com.example.naturelab.backyardbirds.example"

BUNDLE_ID = "com.example"
APP_VERSION = "1.2.3"
ORIGINAL_APP_VERSION = "1.0"
OPAQUE_VALUE = bytes([1, 2, 3, 4, 5, 6, 7, 8])
SHA1_HASH = bytes([0xa1, 0xb2, 0xc3, 0xd4, 0xe5, 0xf6, 0x07, 0x18, 0x29, 0x3a, 0x4b, 0x5c, 0x6d, 0x7e, 0x8f, 0x90, 0x11, 0x22, 0x33, 0x44])
UNKNOWN_RECEIPT_ATTRIBUTE_VALUE = bytes([0x0d, 0x0e, 0x0a, 0x0d])
UNKNOWN_IN_APP_ATTRIBUTE_VALUE = bytes([0x0b, 0x0e, 0x0e, 0x0f])

RECEIPT_CREATION_DATE = "2024-03-01T12:00:00Z"
RECEIPT_CREATION_DATE_MILLIS = 1709294400000
ORIGINAL_PURCHASE_DATE = "2023-11-15T08:30:00Z"
ORIGINAL_PURCHASE_DATE_MILLIS = 1700037000000
EXPIRATION_DATE = "2030-01-01T00:00:00Z"
EXPIRATION_DATE_MILLIS = 1893456000000

CONSUMABLE_PRODUCT_ID = "com.example.coins"
CONSUMABLE_PURCHASE_DATE = "2024-01-15T12:00:00Z"
CONSUMABLE_PURCHASE_DATE_MILLIS = 1705320000000
CONSUMABLE_ORIGINAL_PURCHASE_DATE = "2024-01-10T09:00:00Z"
CONSUMABLE_ORIGINAL_PURCHASE_DATE_MILLIS = 1704877200000

SUBSCRIPTION_PRODUCT_ID = "com.example.subscription"
SUBSCRIPTION_PURCHASE_DATE = "2024-02-01T09:30:00Z"
SUBSCRIPTION_PURCHASE_DATE_MILLIS = 1706779800000
SUBSCRIPTION_EXPIRES_DATE = "2030-02-01T09:30:00Z"
SUBSCRIPTION_EXPIRES_DATE_MILLIS = 1896168600000
SUBSCRIPTION_CANCELLATION_DATE = "2024-06-01T00:00:00Z"
SUBSCRIPTION_CANCELLATION_DATE_MILLIS = 1717200000000

def get_receipt_verifier(creator: ReceiptCreator, environment: Environment, bundle_id: str, enable_online_checks: bool) -> AppReceiptVerifier:
    verifier = AppReceiptVerifier([creator.get_root_certificate()], enable_online_checks, environment, bundle_id)
    verifier._chain_verifier.enable_strict_checks = False # We don't have authority identifiers on test certs
    return verifier

def receipt_payload(receipt_type: str, bundle_id: str, creation_date: str) -> bytes:
    return (AttributeSet()
            .string(0, receipt_type)
            .string(2, bundle_id)
            .string(3, APP_VERSION)
            .raw(4, OPAQUE_VALUE)
            .raw(5, SHA1_HASH)
            .date(12, creation_date)
            .date(18, ORIGINAL_PURCHASE_DATE)
            .string(19, ORIGINAL_APP_VERSION)
            .date(21, EXPIRATION_DATE)
            .raw(9999, UNKNOWN_RECEIPT_ATTRIBUTE_VALUE)
            .raw(17, consumable_purchase())
            .raw(17, subscription_purchase())
            .build())

def consumable_purchase() -> bytes:
    return (AttributeSet()
            .integer(1701, 1)
            .string(1702, CONSUMABLE_PRODUCT_ID)
            .string(1703, "70000000000001")
            .date(1704, CONSUMABLE_PURCHASE_DATE)
            .string(1705, "70000000000001")
            .date(1706, CONSUMABLE_ORIGINAL_PURCHASE_DATE)
            .date(1708, "")
            .integer(1711, 42)
            .date(1712, "")
            .integer(1719, 0)
            .raw(1799, UNKNOWN_IN_APP_ATTRIBUTE_VALUE)
            .build())

def subscription_purchase() -> bytes:
    return (AttributeSet()
            .integer(1701, 1)
            .string(1702, SUBSCRIPTION_PRODUCT_ID)
            .string(1703, "70000000000002")
            .date(1704, SUBSCRIPTION_PURCHASE_DATE)
            .string(1705, "70000000000002")
            .date(1706, SUBSCRIPTION_PURCHASE_DATE)
            .date(1708, SUBSCRIPTION_EXPIRES_DATE)
            .integer(1711, 12345)
            .date(1712, SUBSCRIPTION_CANCELLATION_DATE)
            .integer(1719, 1)
            .build())

def encode_receipt(receipt: bytes) -> str:
    return b64encode(receipt).decode()

class AppReceiptVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt_creator = create_receipt_creator()
        cls.sandbox_receipt = cls.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE))

    def test_app_receipt_decoding(self):
        receipt = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(self.sandbox_receipt))

        self.assertEqual("ProductionSandbox", receipt.receiptType)
        self.assertEqual(BUNDLE_ID, receipt.bundleId)
        self.assertEqual(encode(0x0C, BUNDLE_ID.encode()), receipt.bundleIdBytes)
        self.assertEqual(APP_VERSION, receipt.applicationVersion)
        self.assertEqual(ORIGINAL_APP_VERSION, receipt.originalApplicationVersion)
        self.assertEqual(OPAQUE_VALUE, receipt.opaqueValue)
        self.assertEqual(SHA1_HASH, receipt.sha1Hash)
        self.assertEqual(RECEIPT_CREATION_DATE_MILLIS, receipt.receiptCreationDate)
        self.assertEqual(ORIGINAL_PURCHASE_DATE_MILLIS, receipt.originalPurchaseDate)
        self.assertEqual(EXPIRATION_DATE_MILLIS, receipt.expirationDate)
        self.assertEqual(2, len(receipt.inAppPurchases))

        consumable = receipt.inAppPurchases[0]
        self.assertEqual(1, consumable.quantity)
        self.assertEqual(CONSUMABLE_PRODUCT_ID, consumable.productId)
        self.assertEqual("70000000000001", consumable.transactionId)
        self.assertEqual("70000000000001", consumable.originalTransactionId)
        self.assertEqual(CONSUMABLE_PURCHASE_DATE_MILLIS, consumable.purchaseDate)
        self.assertEqual(CONSUMABLE_ORIGINAL_PURCHASE_DATE_MILLIS, consumable.originalPurchaseDate)
        self.assertEqual(42, consumable.webOrderLineItemId)

        subscription = receipt.inAppPurchases[1]
        self.assertEqual(1, subscription.quantity)
        self.assertEqual(SUBSCRIPTION_PRODUCT_ID, subscription.productId)
        self.assertEqual("70000000000002", subscription.transactionId)
        self.assertEqual("70000000000002", subscription.originalTransactionId)
        self.assertEqual(SUBSCRIPTION_PURCHASE_DATE_MILLIS, subscription.purchaseDate)
        self.assertEqual(SUBSCRIPTION_PURCHASE_DATE_MILLIS, subscription.originalPurchaseDate)
        self.assertEqual(SUBSCRIPTION_EXPIRES_DATE_MILLIS, subscription.expiresDate)
        self.assertEqual(SUBSCRIPTION_CANCELLATION_DATE_MILLIS, subscription.cancellationDate)
        self.assertEqual(12345, subscription.webOrderLineItemId)

    def test_in_app_purchase_flag_and_empty_date_decoding(self):
        # An in-app purchase attribute that is present but empty means "absent", and the intro offer flag is an
        # integer that must surface as a boolean, so a caller can distinguish "no expiration" from "expired at epoch"
        receipt = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(self.sandbox_receipt))

        consumable = receipt.inAppPurchases[0]
        self.assertEqual(False, consumable.isInIntroOfferPeriod)
        self.assertIsNone(consumable.expiresDate)
        self.assertIsNone(consumable.cancellationDate)

        self.assertEqual(True, receipt.inAppPurchases[1].isInIntroOfferPeriod)

    def test_unknown_attributes_are_preserved(self):
        # Attribute types this library does not model must survive decoding with their raw bytes, so a receipt
        # field Apple adds later stays reachable
        receipt = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(self.sandbox_receipt))

        self.assertEqual([UNKNOWN_RECEIPT_ATTRIBUTE_VALUE], receipt.unknownAttributes[9999])
        self.assertEqual([UNKNOWN_IN_APP_ATTRIBUTE_VALUE], receipt.inAppPurchases[0].unknownAttributes[1799])

    def test_wrong_bundle_id(self):
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, "com.example.other", False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(self.sandbox_receipt))
        self.assertEqual(VerificationStatus.INVALID_APP_IDENTIFIER, context.exception.status)

    def test_wrong_environment(self):
        production_receipt = self.receipt_creator.sign_receipt(receipt_payload("Production", BUNDLE_ID, RECEIPT_CREATION_DATE))
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(production_receipt))
        self.assertEqual(VerificationStatus.INVALID_ENVIRONMENT, context.exception.status)

    def test_unknown_receipt_type(self):
        # A receipt type this library does not recognize maps to no environment at all rather than defaulting to
        # the verifier's, so an unexpected value can never be mistaken for a match
        unknown_type_receipt = self.receipt_creator.sign_receipt(receipt_payload("ProductionInternal", BUNDLE_ID, RECEIPT_CREATION_DATE))
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(unknown_type_receipt))
        self.assertEqual(VerificationStatus.INVALID_ENVIRONMENT, context.exception.status)

    def test_tampered_payload(self):
        tampered_receipt = bytearray(self.sandbox_receipt)
        # Flip a bit inside the app version of the encapsulated payload; the chain is untouched, so only the
        # signature check can catch this
        tampered_receipt[tampered_receipt.index(APP_VERSION.encode())] ^= 0x01
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(bytes(tampered_receipt)))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_receipt_signed_by_foreign_root(self):
        foreign_creator = create_receipt_creator()
        forged_receipt = foreign_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE))
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(forged_receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_leaf_without_receipt_signing_oid(self):
        creator = create_receipt_creator(False, True, days_ago(3650), in_one_year())
        receipt = creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE))
        verifier = get_receipt_verifier(creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_intermediate_without_wwdr_oid(self):
        creator = create_receipt_creator(True, False, days_ago(3650), in_one_year())
        receipt = creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE))
        verifier = get_receipt_verifier(creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_receipt_without_root_certificate_embedded(self):
        receipt = self.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE), 2)
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.INVALID_CHAIN_LENGTH, context.exception.status)

    def test_receipt_that_is_not_base64(self):
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt("!!!not-base64!!!")
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_receipt_that_is_not_a_pkcs7_container(self):
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(bytes([1, 2, 3, 4])))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_trailing_bytes_after_container(self):
        # Bytes appended after the container must not be ignored, a verifier that parsed a prefix would accept a
        # receipt carrying unverified extra data
        padded_receipt = self.sandbox_receipt + bytes(4)
        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(padded_receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_receipt_signed_by_now_expired_certificates(self):
        # Receipts outlive the certificates that signed them, so with online checks off the chain is evaluated at
        # the receipt's creation date
        expired_creator = create_receipt_creator(True, True, days_ago(730), days_ago(365))
        created_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) - datetime.timedelta(days=547)
        creation_date = created_at.isoformat().replace('+00:00', 'Z')
        receipt = expired_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, creation_date), signing_time=created_at)

        decoded = get_receipt_verifier(expired_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(round(created_at.timestamp() * 1000), decoded.receiptCreationDate)

    def test_receipt_signed_by_now_expired_certificates_with_online_checks(self):
        # Enabling online checks moves the evaluation to now, which is the point of the option: the same receipt
        # must then fail on the expired chain
        expired_creator = create_receipt_creator(True, True, days_ago(730), days_ago(365))
        created_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) - datetime.timedelta(days=547)
        creation_date = created_at.isoformat().replace('+00:00', 'Z')
        receipt = expired_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, creation_date), signing_time=created_at)

        verifier = get_receipt_verifier(expired_creator, Environment.SANDBOX, BUNDLE_ID, True)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_xcode_receipt_decoding(self):
        # Xcode-generated receipts are not signed by the App Store, so they are decoded without any chain or
        # signature check
        xcode_creator = create_self_signed_receipt_creator()
        receipt = xcode_creator.sign_receipt(double_wrap(receipt_payload("Xcode", BUNDLE_ID, RECEIPT_CREATION_DATE)))

        decoded = get_receipt_verifier(xcode_creator, Environment.XCODE, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual("Xcode", decoded.receiptType)
        self.assertEqual(BUNDLE_ID, decoded.bundleId)
        self.assertEqual(APP_VERSION, decoded.applicationVersion)
        self.assertEqual(RECEIPT_CREATION_DATE_MILLIS, decoded.receiptCreationDate)
        self.assertEqual(2, len(decoded.inAppPurchases))

    def test_xcode_receipt_with_wrong_bundle_id(self):
        # Skipping the signature checks must not skip the app identity check
        xcode_creator = create_self_signed_receipt_creator()
        receipt = xcode_creator.sign_receipt(double_wrap(receipt_payload("Xcode", BUNDLE_ID, RECEIPT_CREATION_DATE)))

        verifier = get_receipt_verifier(xcode_creator, Environment.XCODE, "com.example.other", False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.INVALID_APP_IDENTIFIER, context.exception.status)

    def test_xcode_receipt_with_wrong_environment(self):
        # Skipping the signature checks must not skip the environment check either
        xcode_creator = create_self_signed_receipt_creator()
        receipt = xcode_creator.sign_receipt(double_wrap(receipt_payload("Production", BUNDLE_ID, RECEIPT_CREATION_DATE)))

        verifier = get_receipt_verifier(xcode_creator, Environment.XCODE, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.INVALID_ENVIRONMENT, context.exception.status)

    def test_verify_and_extract_transaction_id(self):
        transaction_id = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_extract_transaction_id(encode_receipt(self.sandbox_receipt))
        self.assertEqual("70000000000001", transaction_id)

    def test_verify_and_extract_transaction_id_without_in_app_purchases(self):
        # Same output contract as ReceiptUtility: a verified receipt with no in-app purchases yields None
        receipt = self.receipt_creator.sign_receipt(AttributeSet()
                                                    .string(0, "ProductionSandbox")
                                                    .string(2, BUNDLE_ID)
                                                    .date(12, RECEIPT_CREATION_DATE)
                                                    .build())
        self.assertIsNone(get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_extract_transaction_id(encode_receipt(receipt)))

    def test_verify_and_extract_transaction_id_rejects_foreign_receipt(self):
        # Unlike ReceiptUtility, extraction refuses a receipt that does not verify
        foreign_creator = create_receipt_creator()
        receipt = foreign_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE))

        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_extract_transaction_id(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_receipt_without_signed_attributes(self):
        # Apple's own receipts authenticate no attributes and sign the payload directly, so that branch of the
        # signature check carries production traffic and must verify
        receipt = self.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE), signed_attributes=False)

        decoded = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(BUNDLE_ID, decoded.bundleId)
        self.assertEqual(RECEIPT_CREATION_DATE_MILLIS, decoded.receiptCreationDate)

    def test_tampered_payload_without_signed_attributes(self):
        receipt = bytearray(self.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE), signed_attributes=False))
        receipt[receipt.index(APP_VERSION.encode())] ^= 0x01

        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(bytes(receipt)))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_receipt_with_a_segmented_payload(self):
        # BER splits a long octet string into segments, which the payload of a genuine receipt arrives in, so the
        # segments must be rejoined before either the digest or the payload is read
        receipt = self.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE), content_segment_size=64)

        decoded = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(BUNDLE_ID, decoded.bundleId)
        self.assertEqual(RECEIPT_CREATION_DATE_MILLIS, decoded.receiptCreationDate)
        self.assertEqual(2, len(decoded.inAppPurchases))

    def test_verify_and_extract_transaction_id_falls_back_to_the_original(self):
        # Same output contract as ReceiptUtility, which takes whichever of the two identifiers a purchase carries
        receipt = self.receipt_creator.sign_receipt(AttributeSet()
                                                    .string(0, "ProductionSandbox")
                                                    .string(2, BUNDLE_ID)
                                                    .date(12, RECEIPT_CREATION_DATE)
                                                    .raw(17, AttributeSet().string(1705, "70000000000003").build())
                                                    .build())

        transaction_id = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_extract_transaction_id(encode_receipt(receipt))
        self.assertEqual("70000000000003", transaction_id)

    def test_sha1_signed_receipt(self):
        # Apple has signed receipts with SHA-1, so it stays on the digest allowlist
        receipt = self.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE), digest='sha1')

        decoded = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False).verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(BUNDLE_ID, decoded.bundleId)

    def test_receipt_with_a_digest_apple_does_not_use(self):
        # A correctly signed receipt still fails when the signer names a digest outside the allowlist, so the
        # accepted algorithms never widen to whatever a signer proposes
        receipt = self.receipt_creator.sign_receipt(receipt_payload("ProductionSandbox", BUNDLE_ID, RECEIPT_CREATION_DATE), digest='sha512')

        verifier = get_receipt_verifier(self.receipt_creator, Environment.SANDBOX, BUNDLE_ID, False)
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_app_receipt(encode_receipt(receipt))
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_xcode_generated_app_receipt_decoding(self):
        # A receipt Xcode actually produced, which unlike the synthetic ones above is BER with indefinite lengths,
        # segmented octet strings and a double-wrapped payload
        verifier = AppReceiptVerifier([read_data_from_binary_file('tests/resources/certs/testCA.der')], False, Environment.XCODE, XCODE_BUNDLE_ID)

        receipt = verifier.verify_and_decode_app_receipt(read_data_from_file("tests/resources/xcode/xcode-app-receipt-with-transaction"))

        self.assertEqual("Xcode", receipt.receiptType)
        self.assertEqual(XCODE_BUNDLE_ID, receipt.bundleId)
        self.assertEqual("1", receipt.applicationVersion)
        self.assertEqual(1697679940000, receipt.receiptCreationDate)
        self.assertEqual(1, len(receipt.inAppPurchases))
        purchase = receipt.inAppPurchases[0]
        self.assertEqual(1, purchase.quantity)
        self.assertEqual("pass.premium", purchase.productId)
        self.assertEqual("0", purchase.transactionId)
        self.assertEqual(1697679936000, purchase.purchaseDate)
        self.assertEqual(1700358336000, purchase.expiresDate)
        self.assertEqual(True, purchase.isInIntroOfferPeriod)

    def test_xcode_generated_app_receipt_transaction_id_extraction(self):
        # The output contract this shares with ReceiptUtility, checked against the same receipts
        verifier = AppReceiptVerifier([read_data_from_binary_file('tests/resources/certs/testCA.der')], False, Environment.XCODE, XCODE_BUNDLE_ID)

        self.assertEqual("0", verifier.verify_and_extract_transaction_id(read_data_from_file("tests/resources/xcode/xcode-app-receipt-with-transaction")))
        self.assertIsNone(verifier.verify_and_extract_transaction_id(read_data_from_file("tests/resources/xcode/xcode-app-receipt-empty")))


if __name__ == '__main__':
    unittest.main()
