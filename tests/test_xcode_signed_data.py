# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
from appstoreserverlibrary.models.AutoRenewStatus import AutoRenewStatus
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.InAppOwnershipType import InAppOwnershipType
from appstoreserverlibrary.models.OfferType import OfferType
from appstoreserverlibrary.models.TransactionReason import TransactionReason
from appstoreserverlibrary.models.Type import Type
from appstoreserverlibrary.receipt_utility import ReceiptUtility
from appstoreserverlibrary.signed_data_verifier import VerificationException

from tests.util import get_signed_data_verifier, read_data_from_file

XCODE_BUNDLE_ID = "com.example.naturelab.backyardbirds.example"

class ReceiptUtilityTest(unittest.TestCase):
    def test_xcode_signed_app_transaction(self):
        verifier = get_signed_data_verifier(Environment.XCODE, XCODE_BUNDLE_ID)
        encoded_app_transaction = read_data_from_file("tests/resources/xcode/xcode-signed-app-transaction")

        app_transaction = verifier.verify_and_decode_app_transaction(encoded_app_transaction)

        self.assertIsNotNone(app_transaction)
        self.assertIsNone(app_transaction.appAppleId)
        self.assertEqual(XCODE_BUNDLE_ID, app_transaction.bundleId)
        self.assertEqual("1", app_transaction.applicationVersion)
        self.assertIsNone(app_transaction.versionExternalIdentifier)
        self.assertEqual(-62135769600000, app_transaction.originalPurchaseDate)
        self.assertEqual("1", app_transaction.originalApplicationVersion)
        self.assertEqual("cYUsXc53EbYc0pOeXG5d6/31LGHeVGf84sqSN0OrJi5u/j2H89WWKgS8N0hMsMlf", app_transaction.deviceVerification)
        self.assertEqual("48c8b92d-ce0d-4229-bedf-e61b4f9cfc92", app_transaction.deviceVerificationNonce)
        self.assertIsNone(app_transaction.preorderDate)
        self.assertEqual(Environment.XCODE, app_transaction.receiptType)
        self.assertEqual("Xcode", app_transaction.rawReceiptType)

    def test_xcode_signed_transaction(self):
        verifier = get_signed_data_verifier(Environment.XCODE, XCODE_BUNDLE_ID)
        encoded_transaction = read_data_from_file("tests/resources/xcode/xcode-signed-transaction")

        transaction = verifier.verify_and_decode_signed_transaction(encoded_transaction)

        self.assertEqual("0", transaction.originalTransactionId)
        self.assertEqual("0", transaction.transactionId)
        self.assertEqual("0", transaction.webOrderLineItemId)
        self.assertEqual(XCODE_BUNDLE_ID, transaction.bundleId)
        self.assertEqual("pass.premium", transaction.productId)
        self.assertEqual("6F3A93AB", transaction.subscriptionGroupIdentifier)
        self.assertEqual(1697679936049, transaction.purchaseDate)
        self.assertEqual(1697679936049, transaction.originalPurchaseDate)
        self.assertEqual(1700358336049, transaction.expiresDate)
        self.assertEqual(1, transaction.quantity)
        self.assertEqual(Type.AUTO_RENEWABLE_SUBSCRIPTION, transaction.type)
        self.assertEqual("Auto-Renewable Subscription", transaction.rawType)
        self.assertIsNone(transaction.appAccountToken)
        self.assertEqual(InAppOwnershipType.PURCHASED, transaction.inAppOwnershipType)
        self.assertEqual("PURCHASED", transaction.rawInAppOwnershipType)
        self.assertEqual(1697679936056, transaction.signedDate)
        self.assertIsNone(transaction.revocationReason)
        self.assertIsNone(transaction.revocationDate)
        self.assertFalse(transaction.isUpgraded)
        self.assertEqual(OfferType.INTRODUCTORY_OFFER, transaction.offerType)
        self.assertEqual(1, transaction.rawOfferType)
        self.assertIsNone(transaction.offerIdentifier)
        self.assertEqual(Environment.XCODE, transaction.environment)
        self.assertEqual("Xcode", transaction.rawEnvironment)
        self.assertEqual("USA", transaction.storefront)
        self.assertEqual("143441", transaction.storefrontId)
        self.assertEqual(TransactionReason.PURCHASE, transaction.transactionReason)
        self.assertEqual("PURCHASE", transaction.rawTransactionReason)

    def test_xcode_signed_renewal_info(self):
        verifier = get_signed_data_verifier(Environment.XCODE, XCODE_BUNDLE_ID)
        encoded_renewal_info = read_data_from_file("tests/resources/xcode/xcode-signed-renewal-info")

        renewal_info = verifier.verify_and_decode_renewal_info(encoded_renewal_info)

        self.assertIsNone(renewal_info.expirationIntent)
        self.assertEqual("0", renewal_info.originalTransactionId)
        self.assertEqual("pass.premium", renewal_info.autoRenewProductId)
        self.assertEqual("pass.premium", renewal_info.productId)
        self.assertEqual(AutoRenewStatus.ON, renewal_info.autoRenewStatus)
        self.assertEqual(1, renewal_info.rawAutoRenewStatus)
        self.assertIsNone(renewal_info.isInBillingRetryPeriod)
        self.assertIsNone(renewal_info.priceIncreaseStatus)
        self.assertIsNone(renewal_info.gracePeriodExpiresDate)
        self.assertIsNone(renewal_info.offerType)
        self.assertIsNone(renewal_info.offerIdentifier)
        self.assertEqual(1697679936711, renewal_info.signedDate)
        self.assertEqual(Environment.XCODE, renewal_info.environment)
        self.assertEqual("Xcode", renewal_info.rawEnvironment)
        self.assertEqual(1697679936049, renewal_info.recentSubscriptionStartDate)
        self.assertEqual(1700358336049, renewal_info.renewalDate)

    def test_xcode_signed_app_transaction_with_production_environment(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, XCODE_BUNDLE_ID)
        encoded_app_transaction = read_data_from_file("tests/resources/xcode/xcode-signed-app-transaction")
        try:
            verifier.verify_and_decode_app_transaction(encoded_app_transaction)
        except VerificationException:
            return
        self.assertFalse(True)

