# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
import unittest
from appstoreserverlibrary.models.AutoRenewStatus import AutoRenewStatus
from appstoreserverlibrary.models.ConsumptionRequestReason import ConsumptionRequestReason
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.ExpirationIntent import ExpirationIntent
from appstoreserverlibrary.models.InAppOwnershipType import InAppOwnershipType
from appstoreserverlibrary.models.NotificationTypeV2 import NotificationTypeV2
from appstoreserverlibrary.models.OfferDiscountType import OfferDiscountType
from appstoreserverlibrary.models.OfferType import OfferType
from appstoreserverlibrary.models.PriceIncreaseStatus import PriceIncreaseStatus
from appstoreserverlibrary.models.RevocationReason import RevocationReason
from appstoreserverlibrary.models.Status import Status
from appstoreserverlibrary.models.Subtype import Subtype
from appstoreserverlibrary.models.TransactionReason import TransactionReason
from appstoreserverlibrary.models.Type import Type

from tests.util import create_signed_data_from_json, get_default_signed_data_verifier, get_signed_data_verifier

class DecodedPayloads(unittest.TestCase):
    def test_app_transaction_decoding(self):
        signed_app_transaction = create_signed_data_from_json('tests/resources/models/appTransaction.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        app_transaction = signed_data_verifier.verify_and_decode_app_transaction(signed_app_transaction)
        self.assertEqual(Environment.LOCAL_TESTING, app_transaction.receiptType)
        self.assertEqual("LocalTesting", app_transaction.rawReceiptType)
        self.assertEqual(531412, app_transaction.appAppleId)
        self.assertEqual("com.example", app_transaction.bundleId)
        self.assertEqual("1.2.3", app_transaction.applicationVersion)
        self.assertEqual(512, app_transaction.versionExternalIdentifier)
        self.assertEqual(1698148900000, app_transaction.receiptCreationDate)
        self.assertEqual(1698148800000, app_transaction.originalPurchaseDate)
        self.assertEqual("1.1.2", app_transaction.originalApplicationVersion)
        self.assertEqual("device_verification_value", app_transaction.deviceVerification)
        self.assertEqual("48ccfa42-7431-4f22-9908-7e88983e105a", app_transaction.deviceVerificationNonce)
        self.assertEqual(1698148700000, app_transaction.preorderDate)

    def test_transaction_decoding(self):
        signed_transaction = create_signed_data_from_json('tests/resources/models/signedTransaction.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        transaction = signed_data_verifier.verify_and_decode_signed_transaction(signed_transaction)
        
        self.assertEqual("12345", transaction.originalTransactionId)
        self.assertEqual("23456", transaction.transactionId)
        self.assertEqual("34343", transaction.webOrderLineItemId)
        self.assertEqual("com.example", transaction.bundleId)
        self.assertEqual("com.example.product", transaction.productId)
        self.assertEqual("55555", transaction.subscriptionGroupIdentifier)
        self.assertEqual(1698148800000, transaction.originalPurchaseDate)
        self.assertEqual(1698148900000, transaction.purchaseDate)
        self.assertEqual(1698148950000, transaction.revocationDate)
        self.assertEqual(1698149000000, transaction.expiresDate)
        self.assertEqual(1, transaction.quantity)
        self.assertEqual(Type.AUTO_RENEWABLE_SUBSCRIPTION, transaction.type)
        self.assertEqual("Auto-Renewable Subscription", transaction.rawType)
        self.assertEqual("7e3fb20b-4cdb-47cc-936d-99d65f608138", transaction.appAccountToken)
        self.assertEqual(InAppOwnershipType.PURCHASED, transaction.inAppOwnershipType)
        self.assertEqual("PURCHASED", transaction.rawInAppOwnershipType)
        self.assertEqual(1698148900000, transaction.signedDate)
        self.assertEqual(RevocationReason.REFUNDED_DUE_TO_ISSUE, transaction.revocationReason)
        self.assertEqual(1, transaction.rawRevocationReason)
        self.assertEqual("abc.123", transaction.offerIdentifier)
        self.assertTrue(transaction.isUpgraded)
        self.assertEqual(OfferType.INTRODUCTORY_OFFER, transaction.offerType)
        self.assertEqual(1, transaction.rawOfferType)
        self.assertEqual("USA", transaction.storefront)
        self.assertEqual("143441", transaction.storefrontId)
        self.assertEqual(TransactionReason.PURCHASE, transaction.transactionReason)
        self.assertEqual("PURCHASE", transaction.rawTransactionReason)
        self.assertEqual(Environment.LOCAL_TESTING, transaction.environment)
        self.assertEqual("LocalTesting", transaction.rawEnvironment)
        self.assertEqual(10990, transaction.price)
        self.assertEqual("USD", transaction.currency)
        self.assertEqual(OfferDiscountType.PAY_AS_YOU_GO, transaction.offerDiscountType)
        self.assertEqual("PAY_AS_YOU_GO", transaction.rawOfferDiscountType)

    
    def test_renewal_info_decoding(self):
        signed_renewal_info = create_signed_data_from_json('tests/resources/models/signedRenewalInfo.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        renewal_info = signed_data_verifier.verify_and_decode_renewal_info(signed_renewal_info)

        self.assertEqual(ExpirationIntent.CUSTOMER_CANCELLED, renewal_info.expirationIntent)
        self.assertEqual(1, renewal_info.rawExpirationIntent)
        self.assertEqual("12345", renewal_info.originalTransactionId)
        self.assertEqual("com.example.product.2", renewal_info.autoRenewProductId)
        self.assertEqual("com.example.product", renewal_info.productId)
        self.assertEqual(AutoRenewStatus.ON, renewal_info.autoRenewStatus)
        self.assertEqual(1, renewal_info.rawAutoRenewStatus)
        self.assertTrue(renewal_info.isInBillingRetryPeriod)
        self.assertEqual(PriceIncreaseStatus.CUSTOMER_HAS_NOT_RESPONDED, renewal_info.priceIncreaseStatus)
        self.assertEqual(0, renewal_info.rawPriceIncreaseStatus)
        self.assertEqual(1698148900000, renewal_info.gracePeriodExpiresDate)
        self.assertEqual(OfferType.PROMOTIONAL_OFFER, renewal_info.offerType)
        self.assertEqual(2, renewal_info.rawOfferType)
        self.assertEqual("abc.123", renewal_info.offerIdentifier)
        self.assertEqual(1698148800000, renewal_info.signedDate)
        self.assertEqual(Environment.LOCAL_TESTING, renewal_info.environment)
        self.assertEqual("LocalTesting", renewal_info.rawEnvironment)
        self.assertEqual(1698148800000, renewal_info.recentSubscriptionStartDate)
        self.assertEqual(1698148850000, renewal_info.renewalDate)
        self.assertEqual(9990, renewal_info.renewalPrice)
        self.assertEqual("USD", renewal_info.currency)
        self.assertEqual(OfferDiscountType.PAY_AS_YOU_GO, renewal_info.offerDiscountType)
        self.assertEqual("PAY_AS_YOU_GO", renewal_info.rawOfferDiscountType)
        self.assertEqual(['eligible1', 'eligible2'], renewal_info.eligibleWinBackOfferIds)

    def test_notification_decoding(self):
        signed_notification = create_signed_data_from_json('tests/resources/models/signedNotification.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        notification = signed_data_verifier.verify_and_decode_notification(signed_notification)

        self.assertEqual(NotificationTypeV2.SUBSCRIBED, notification.notificationType)
        self.assertEqual("SUBSCRIBED", notification.rawNotificationType)
        self.assertEqual(Subtype.INITIAL_BUY, notification.subtype)
        self.assertEqual("INITIAL_BUY", notification.rawSubtype)
        self.assertEqual("002e14d5-51f5-4503-b5a8-c3a1af68eb20", notification.notificationUUID)
        self.assertEqual("2.0", notification.version)
        self.assertEqual(1698148900000, notification.signedDate)
        self.assertIsNotNone(notification.data)
        self.assertIsNone(notification.summary)
        self.assertIsNone(notification.externalPurchaseToken)
        self.assertEqual(Environment.LOCAL_TESTING, notification.data.environment)
        self.assertEqual("LocalTesting", notification.data.rawEnvironment)
        self.assertEqual(41234, notification.data.appAppleId)
        self.assertEqual("com.example", notification.data.bundleId)
        self.assertEqual("1.2.3", notification.data.bundleVersion)
        self.assertEqual("signed_transaction_info_value", notification.data.signedTransactionInfo)
        self.assertEqual("signed_renewal_info_value", notification.data.signedRenewalInfo);
        self.assertEqual(Status.ACTIVE, notification.data.status)
        self.assertEqual(1, notification.data.rawStatus)
        self.assertIsNone(notification.data.consumptionRequestReason)
        self.assertIsNone(notification.data.rawConsumptionRequestReason)

    def test_consumption_request_notification_decoding(self):
        signed_notification = create_signed_data_from_json('tests/resources/models/signedConsumptionRequestNotification.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        notification = signed_data_verifier.verify_and_decode_notification(signed_notification)

        self.assertEqual(NotificationTypeV2.CONSUMPTION_REQUEST, notification.notificationType)
        self.assertEqual("CONSUMPTION_REQUEST", notification.rawNotificationType)
        self.assertIsNone(notification.subtype)
        self.assertIsNone(notification.rawSubtype)
        self.assertEqual("002e14d5-51f5-4503-b5a8-c3a1af68eb20", notification.notificationUUID)
        self.assertEqual("2.0", notification.version)
        self.assertEqual(1698148900000, notification.signedDate)
        self.assertIsNotNone(notification.data)
        self.assertIsNone(notification.summary)
        self.assertIsNone(notification.externalPurchaseToken)
        self.assertEqual(Environment.LOCAL_TESTING, notification.data.environment)
        self.assertEqual("LocalTesting", notification.data.rawEnvironment)
        self.assertEqual(41234, notification.data.appAppleId)
        self.assertEqual("com.example", notification.data.bundleId)
        self.assertEqual("1.2.3", notification.data.bundleVersion)
        self.assertEqual("signed_transaction_info_value", notification.data.signedTransactionInfo)
        self.assertEqual("signed_renewal_info_value", notification.data.signedRenewalInfo);
        self.assertEqual(Status.ACTIVE, notification.data.status)
        self.assertEqual(1, notification.data.rawStatus)
        self.assertEqual(ConsumptionRequestReason.UNINTENDED_PURCHASE, notification.data.consumptionRequestReason)
        self.assertEqual("UNINTENDED_PURCHASE", notification.data.rawConsumptionRequestReason)
        
    def test_summary_notification_decoding(self):
        signed_summary_notification = create_signed_data_from_json('tests/resources/models/signedSummaryNotification.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        notification = signed_data_verifier.verify_and_decode_notification(signed_summary_notification)
        
        self.assertEqual(NotificationTypeV2.RENEWAL_EXTENSION, notification.notificationType)
        self.assertEqual("RENEWAL_EXTENSION", notification.rawNotificationType)
        self.assertEqual(Subtype.SUMMARY, notification.subtype)
        self.assertEqual("SUMMARY", notification.rawSubtype)
        self.assertEqual("002e14d5-51f5-4503-b5a8-c3a1af68eb20", notification.notificationUUID)
        self.assertEqual("2.0", notification.version)
        self.assertEqual(1698148900000, notification.signedDate)
        self.assertIsNone(notification.data)
        self.assertIsNotNone(notification.summary)
        self.assertIsNone(notification.externalPurchaseToken)
        self.assertEqual(Environment.LOCAL_TESTING, notification.summary.environment)
        self.assertEqual("LocalTesting", notification.summary.rawEnvironment)
        self.assertEqual(41234, notification.summary.appAppleId)
        self.assertEqual("com.example", notification.summary.bundleId)
        self.assertEqual("com.example.product", notification.summary.productId)
        self.assertEqual("efb27071-45a4-4aca-9854-2a1e9146f265", notification.summary.requestIdentifier)
        self.assertEqual(["CAN", "USA", "MEX"], notification.summary.storefrontCountryCodes)
        self.assertEqual(5, notification.summary.succeededCount)
        self.assertEqual(2, notification.summary.failedCount)
    
    def test_external_purchase_token_notification_decoding(self):
        signed_external_purchase_token_notification = create_signed_data_from_json('tests/resources/models/signedExternalPurchaseTokenNotification.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        def check_environment_and_bundle_id(bundle_id: Optional[str], app_apple_id: Optional[int], environment: Optional[Environment]):
            self.assertEqual("com.example", bundle_id)
            self.assertEqual(55555, app_apple_id)
            self.assertEqual(Environment.PRODUCTION, environment)

        signed_data_verifier._verify_notification = check_environment_and_bundle_id

        notification = signed_data_verifier.verify_and_decode_notification(signed_external_purchase_token_notification)
        
        self.assertEqual(NotificationTypeV2.EXTERNAL_PURCHASE_TOKEN, notification.notificationType)
        self.assertEqual("EXTERNAL_PURCHASE_TOKEN", notification.rawNotificationType)
        self.assertEqual(Subtype.UNREPORTED, notification.subtype)
        self.assertEqual("UNREPORTED", notification.rawSubtype)
        self.assertEqual("002e14d5-51f5-4503-b5a8-c3a1af68eb20", notification.notificationUUID)
        self.assertEqual("2.0", notification.version)
        self.assertEqual(1698148900000, notification.signedDate)
        self.assertIsNone(notification.data)
        self.assertIsNone(notification.summary)
        self.assertIsNotNone(notification.externalPurchaseToken)
        self.assertEqual("b2158121-7af9-49d4-9561-1f588205523e", notification.externalPurchaseToken.externalPurchaseId)
        self.assertEqual(1698148950000, notification.externalPurchaseToken.tokenCreationDate)
        self.assertEqual(55555, notification.externalPurchaseToken.appAppleId)
        self.assertEqual("com.example", notification.externalPurchaseToken.bundleId)
    
    def test_external_purchase_token_sandbox_notification_decoding(self):
        signed_external_purchase_token_notification = create_signed_data_from_json('tests/resources/models/signedExternalPurchaseTokenSandboxNotification.json')
        
        signed_data_verifier = get_default_signed_data_verifier()

        def check_environment_and_bundle_id(bundle_id: Optional[str], app_apple_id: Optional[int], environment: Optional[Environment]):
            self.assertEqual("com.example", bundle_id)
            self.assertEqual(55555, app_apple_id)
            self.assertEqual(Environment.SANDBOX, environment)

        signed_data_verifier._verify_notification = check_environment_and_bundle_id

        notification = signed_data_verifier.verify_and_decode_notification(signed_external_purchase_token_notification)
        
        self.assertEqual(NotificationTypeV2.EXTERNAL_PURCHASE_TOKEN, notification.notificationType)
        self.assertEqual("EXTERNAL_PURCHASE_TOKEN", notification.rawNotificationType)
        self.assertEqual(Subtype.UNREPORTED, notification.subtype)
        self.assertEqual("UNREPORTED", notification.rawSubtype)
        self.assertEqual("002e14d5-51f5-4503-b5a8-c3a1af68eb20", notification.notificationUUID)
        self.assertEqual("2.0", notification.version)
        self.assertEqual(1698148900000, notification.signedDate)
        self.assertIsNone(notification.data)
        self.assertIsNone(notification.summary)
        self.assertIsNotNone(notification.externalPurchaseToken)
        self.assertEqual("SANDBOX_b2158121-7af9-49d4-9561-1f588205523e", notification.externalPurchaseToken.externalPurchaseId)
        self.assertEqual(1698148950000, notification.externalPurchaseToken.tokenCreationDate)
        self.assertEqual(55555, notification.externalPurchaseToken.appAppleId)
        self.assertEqual("com.example", notification.externalPurchaseToken.bundleId)