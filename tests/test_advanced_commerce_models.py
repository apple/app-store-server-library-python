# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import json
import unittest

from appstoreserverlibrary.models.AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from appstoreserverlibrary.models.AdvancedCommerceEffective import AdvancedCommerceEffective
from appstoreserverlibrary.models.AdvancedCommerceOffer import AdvancedCommerceOffer
from appstoreserverlibrary.models.AdvancedCommerceOfferPeriod import AdvancedCommerceOfferPeriod
from appstoreserverlibrary.models.AdvancedCommerceOfferReason import AdvancedCommerceOfferReason
from appstoreserverlibrary.models.AdvancedCommerceOneTimeChargeCreateRequest import AdvancedCommerceOneTimeChargeCreateRequest
from appstoreserverlibrary.models.AdvancedCommerceOneTimeChargeItem import AdvancedCommerceOneTimeChargeItem
from appstoreserverlibrary.models.AdvancedCommercePeriod import AdvancedCommercePeriod
from appstoreserverlibrary.models.AdvancedCommerceReason import AdvancedCommerceReason
from appstoreserverlibrary.models.AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from appstoreserverlibrary.models.AdvancedCommerceRefundType import AdvancedCommerceRefundType
from appstoreserverlibrary.models.AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from appstoreserverlibrary.models.AdvancedCommerceRequestRefundItem import AdvancedCommerceRequestRefundItem
from appstoreserverlibrary.models.AdvancedCommerceRequestRefundRequest import AdvancedCommerceRequestRefundRequest
from appstoreserverlibrary.models.AdvancedCommerceRequestRefundResponse import AdvancedCommerceRequestRefundResponse
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionCancelRequest import AdvancedCommerceSubscriptionCancelRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionCancelResponse import AdvancedCommerceSubscriptionCancelResponse
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionChangeMetadataDescriptors import AdvancedCommerceSubscriptionChangeMetadataDescriptors
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionChangeMetadataItem import AdvancedCommerceSubscriptionChangeMetadataItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionChangeMetadataRequest import AdvancedCommerceSubscriptionChangeMetadataRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionChangeMetadataResponse import AdvancedCommerceSubscriptionChangeMetadataResponse
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionCreateItem import AdvancedCommerceSubscriptionCreateItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionCreateRequest import AdvancedCommerceSubscriptionCreateRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionMigrateDescriptors import AdvancedCommerceSubscriptionMigrateDescriptors
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionMigrateItem import AdvancedCommerceSubscriptionMigrateItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionMigrateRenewalItem import AdvancedCommerceSubscriptionMigrateRenewalItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionMigrateRequest import AdvancedCommerceSubscriptionMigrateRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionMigrateResponse import AdvancedCommerceSubscriptionMigrateResponse
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyAddItem import AdvancedCommerceSubscriptionModifyAddItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyChangeItem import AdvancedCommerceSubscriptionModifyChangeItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyDescriptors import AdvancedCommerceSubscriptionModifyDescriptors
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyInAppRequest import AdvancedCommerceSubscriptionModifyInAppRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyPeriodChange import AdvancedCommerceSubscriptionModifyPeriodChange
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyRemoveItem import AdvancedCommerceSubscriptionModifyRemoveItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionPriceChangeItem import AdvancedCommerceSubscriptionPriceChangeItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionPriceChangeRequest import AdvancedCommerceSubscriptionPriceChangeRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionPriceChangeResponse import AdvancedCommerceSubscriptionPriceChangeResponse
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionReactivateInAppRequest import AdvancedCommerceSubscriptionReactivateInAppRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionReactivateItem import AdvancedCommerceSubscriptionReactivateItem
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionRevokeRequest import AdvancedCommerceSubscriptionRevokeRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionRevokeResponse import AdvancedCommerceSubscriptionRevokeResponse
from appstoreserverlibrary.models.AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter
from tests.util import read_data_from_file


class AdvancedCommerceModelsTest(unittest.TestCase):
    def test_advanced_commerce_period(self):
        self.assertEqual("P1W", AdvancedCommercePeriod.P1W.value)
        self.assertEqual("P1M", AdvancedCommercePeriod.P1M.value)
        self.assertEqual("P2M", AdvancedCommercePeriod.P2M.value)
        self.assertEqual("P3M", AdvancedCommercePeriod.P3M.value)
        self.assertEqual("P6M", AdvancedCommercePeriod.P6M.value)
        self.assertEqual("P1Y", AdvancedCommercePeriod.P1Y.value)

        self.assertEqual(AdvancedCommercePeriod.P1W, AdvancedCommercePeriod("P1W"))
        self.assertEqual(AdvancedCommercePeriod.P1M, AdvancedCommercePeriod("P1M"))
        self.assertEqual(AdvancedCommercePeriod.P1Y, AdvancedCommercePeriod("P1Y"))
        self.assertFalse("INVALID" in AdvancedCommercePeriod)

        self.assertEqual("P1W", AdvancedCommercePeriod.P1W.value)

    def test_advanced_commerce_reason(self):
        self.assertEqual("UPGRADE", AdvancedCommerceReason.UPGRADE.value)
        self.assertEqual("DOWNGRADE", AdvancedCommerceReason.DOWNGRADE.value)
        self.assertEqual("APPLY_OFFER", AdvancedCommerceReason.APPLY_OFFER.value)

        self.assertEqual(AdvancedCommerceReason.UPGRADE, AdvancedCommerceReason("UPGRADE"))
        self.assertEqual(AdvancedCommerceReason.DOWNGRADE, AdvancedCommerceReason("DOWNGRADE"))
        self.assertEqual(AdvancedCommerceReason.APPLY_OFFER, AdvancedCommerceReason("APPLY_OFFER"))
        self.assertFalse("INVALID" in AdvancedCommerceReason)

        self.assertEqual("UPGRADE", AdvancedCommerceReason.UPGRADE.value)

    def test_advanced_commerce_refund_reason(self):
        self.assertEqual("UNINTENDED_PURCHASE", AdvancedCommerceRefundReason.UNINTENDED_PURCHASE.value)
        self.assertEqual("FULFILLMENT_ISSUE", AdvancedCommerceRefundReason.FULFILLMENT_ISSUE.value)
        self.assertEqual("UNSATISFIED_WITH_PURCHASE", AdvancedCommerceRefundReason.UNSATISFIED_WITH_PURCHASE.value)
        self.assertEqual("LEGAL", AdvancedCommerceRefundReason.LEGAL.value)
        self.assertEqual("OTHER", AdvancedCommerceRefundReason.OTHER.value)
        self.assertEqual("MODIFY_ITEMS_REFUND", AdvancedCommerceRefundReason.MODIFY_ITEMS_REFUND.value)
        self.assertEqual("SIMULATE_REFUND_DECLINE", AdvancedCommerceRefundReason.SIMULATE_REFUND_DECLINE.value)

        self.assertEqual(AdvancedCommerceRefundReason.LEGAL, AdvancedCommerceRefundReason("LEGAL"))
        self.assertEqual(AdvancedCommerceRefundReason.OTHER, AdvancedCommerceRefundReason("OTHER"))
        self.assertFalse("INVALID" in AdvancedCommerceRefundReason)

        self.assertEqual("LEGAL", AdvancedCommerceRefundReason.LEGAL.value)

    def test_advanced_commerce_refund_type(self):
        self.assertEqual("FULL", AdvancedCommerceRefundType.FULL.value)
        self.assertEqual("PRORATED", AdvancedCommerceRefundType.PRORATED.value)
        self.assertEqual("CUSTOM", AdvancedCommerceRefundType.CUSTOM.value)

        self.assertEqual(AdvancedCommerceRefundType.FULL, AdvancedCommerceRefundType("FULL"))
        self.assertEqual(AdvancedCommerceRefundType.PRORATED, AdvancedCommerceRefundType("PRORATED"))
        self.assertEqual(AdvancedCommerceRefundType.CUSTOM, AdvancedCommerceRefundType("CUSTOM"))
        self.assertFalse("INVALID" in AdvancedCommerceRefundType)

        self.assertEqual("FULL", AdvancedCommerceRefundType.FULL.value)

    def test_advanced_commerce_offer_period(self):
        self.assertEqual("P3D", AdvancedCommerceOfferPeriod.P3D.value)
        self.assertEqual("P1W", AdvancedCommerceOfferPeriod.P1W.value)
        self.assertEqual("P2W", AdvancedCommerceOfferPeriod.P2W.value)
        self.assertEqual("P1M", AdvancedCommerceOfferPeriod.P1M.value)
        self.assertEqual("P2M", AdvancedCommerceOfferPeriod.P2M.value)
        self.assertEqual("P3M", AdvancedCommerceOfferPeriod.P3M.value)

        self.assertEqual(AdvancedCommerceOfferPeriod.P1W, AdvancedCommerceOfferPeriod("P1W"))
        self.assertEqual(AdvancedCommerceOfferPeriod.P1M, AdvancedCommerceOfferPeriod("P1M"))
        self.assertEqual(AdvancedCommerceOfferPeriod.P3D, AdvancedCommerceOfferPeriod("P3D"))
        self.assertFalse("INVALID" in AdvancedCommerceOfferPeriod)

        self.assertEqual("P1W", AdvancedCommerceOfferPeriod.P1W.value)

    def test_advanced_commerce_offer_reason(self):
        self.assertEqual("ACQUISITION", AdvancedCommerceOfferReason.ACQUISITION.value)
        self.assertEqual("WIN_BACK", AdvancedCommerceOfferReason.WIN_BACK.value)
        self.assertEqual("RETENTION", AdvancedCommerceOfferReason.RETENTION.value)

        self.assertEqual(AdvancedCommerceOfferReason.ACQUISITION, AdvancedCommerceOfferReason("ACQUISITION"))
        self.assertEqual(AdvancedCommerceOfferReason.WIN_BACK, AdvancedCommerceOfferReason("WIN_BACK"))
        self.assertEqual(AdvancedCommerceOfferReason.RETENTION, AdvancedCommerceOfferReason("RETENTION"))
        self.assertFalse("INVALID" in AdvancedCommerceOfferReason)

        self.assertEqual("WIN_BACK", AdvancedCommerceOfferReason.WIN_BACK.value)

    def test_advanced_commerce_effective(self):
        self.assertEqual("IMMEDIATELY", AdvancedCommerceEffective.IMMEDIATELY.value)
        self.assertEqual("NEXT_BILL_CYCLE", AdvancedCommerceEffective.NEXT_BILL_CYCLE.value)

        self.assertEqual(AdvancedCommerceEffective.IMMEDIATELY, AdvancedCommerceEffective("IMMEDIATELY"))
        self.assertEqual(AdvancedCommerceEffective.NEXT_BILL_CYCLE, AdvancedCommerceEffective("NEXT_BILL_CYCLE"))
        self.assertFalse("INVALID" in AdvancedCommerceEffective)

        self.assertEqual("IMMEDIATELY", AdvancedCommerceEffective.IMMEDIATELY.value)

    def test_validation_utils_description(self):
        valid_description = "Valid description"
        AdvancedCommerceValidationUtils.description_validator(None, None, valid_description)

        max_length_description = "A" * 45
        AdvancedCommerceValidationUtils.description_validator(None, None, max_length_description)

        too_long_description = "A" * 46
        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.description_validator(None, None, too_long_description)

    def test_validation_utils_display_name(self):
        valid_display_name = "Valid Name"
        AdvancedCommerceValidationUtils.display_name_validator(None, None, valid_display_name)

        max_length_display_name = "A" * 30
        AdvancedCommerceValidationUtils.display_name_validator(None, None, max_length_display_name)

        too_long_display_name = "A" * 31
        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.display_name_validator(None, None, too_long_display_name)

    def test_validation_utils_sku(self):
        valid_sku = "valid.sku.123"
        AdvancedCommerceValidationUtils.sku_validator(None, None, valid_sku)

        max_length_sku = "A" * 128
        AdvancedCommerceValidationUtils.sku_validator(None, None, max_length_sku)

        too_long_sku = "A" * 129
        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.sku_validator(None, None, too_long_sku)

    def test_validation_utils_period_count(self):
        AdvancedCommerceValidationUtils.period_count_validator(None, None, 1)
        AdvancedCommerceValidationUtils.period_count_validator(None, None, 6)
        AdvancedCommerceValidationUtils.period_count_validator(None, None, 12)

        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.period_count_validator(None, None, 0)

        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.period_count_validator(None, None, 13)

    def test_validation_utils_items(self):
        valid_list = [
            AdvancedCommerceOneTimeChargeItem(
                description="desc",
                displayName="name",
                SKU="sku1",
                price=1000
            )
        ]
        AdvancedCommerceValidationUtils.items_validator(None, None, valid_list)

        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.items_validator(None, None, None)

        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.items_validator(None, None, [])

        list_with_none = [None]
        with self.assertRaises(ValueError):
            AdvancedCommerceValidationUtils.items_validator(None, None, list_with_none)

    def test_advanced_commerce_descriptors_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceDescriptors.json')

        descriptors_dict = json.loads(json_data)
        descriptors = _get_cattrs_converter(AdvancedCommerceDescriptors).structure(descriptors_dict, AdvancedCommerceDescriptors)

        self.assertEqual("description", descriptors.description)
        self.assertEqual("display name", descriptors.displayName)
    
    def test_advanced_commerce_one_time_charge_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceOneTimeChargeItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceOneTimeChargeItem).structure(item_dict, AdvancedCommerceOneTimeChargeItem)

        self.assertEqual("description", item.description)
        self.assertEqual("display name", item.displayName)
        self.assertEqual("sku", item.SKU)
        self.assertEqual(15000, item.price)
    
    def test_advanced_commerce_subscription_create_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCreateItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionCreateItem).structure(item_dict, AdvancedCommerceSubscriptionCreateItem)

        self.assertEqual("description", item.description)
        self.assertEqual("display name", item.displayName)
        self.assertEqual("sku", item.SKU)
        self.assertEqual(20000, item.price)
    
    def test_advanced_commerce_request_refund_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceRequestRefundItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceRequestRefundItem).structure(item_dict, AdvancedCommerceRequestRefundItem)

        self.assertEqual("sku", item.SKU)
        self.assertEqual(AdvancedCommerceRefundReason.LEGAL, item.refundReason)
        self.assertEqual("LEGAL", item.rawRefundReason)
        self.assertEqual(AdvancedCommerceRefundType.FULL, item.refundType)
        self.assertEqual("FULL", item.rawRefundType)
        self.assertTrue(item.revoke)
        self.assertEqual(5000, item.refundAmount)

    def test_advanced_commerce_offer_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceOffer.json')

        offer_dict = json.loads(json_data)
        offer = _get_cattrs_converter(AdvancedCommerceOffer).structure(offer_dict, AdvancedCommerceOffer)

        self.assertEqual(AdvancedCommerceOfferPeriod.P1W, offer.period)
        self.assertEqual("P1W", offer.rawPeriod)
        self.assertEqual(3, offer.periodCount)
        self.assertEqual(5000, offer.price)
        self.assertEqual(AdvancedCommerceOfferReason.WIN_BACK, offer.reason)
        self.assertEqual("WIN_BACK", offer.rawReason)

    def test_advanced_commerce_one_time_charge_create_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceOneTimeChargeCreateRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceOneTimeChargeCreateRequest).structure(request_dict, AdvancedCommerceOneTimeChargeCreateRequest)

        self.assertEqual("USD", request.currency)
        self.assertIsNotNone(request.item)
        self.assertEqual("description", request.item.description)
        self.assertEqual("display name", request.item.displayName)
        self.assertEqual("sku", request.item.SKU)
        self.assertEqual(10000, request.item.price)
        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440000", str(request.requestInfo.requestReferenceId))
        self.assertEqual("taxCode", request.taxCode)
        self.assertEqual("USA", request.storefront)
        self.assertEqual("CREATE_ONE_TIME_CHARGE", request.operation)
        self.assertEqual("1", request.version)
    
    def test_advanced_commerce_subscription_create_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCreateRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionCreateRequest).structure(request_dict, AdvancedCommerceSubscriptionCreateRequest)

        self.assertEqual("USD", request.currency)
        self.assertIsNotNone(request.descriptors)
        self.assertEqual("description", request.descriptors.description)
        self.assertEqual("display name", request.descriptors.displayName)
        self.assertEqual(2, len(request.items))
        self.assertEqual("sku", request.items[0].SKU)
        self.assertEqual(20000, request.items[0].price)
        self.assertEqual("sku", request.items[1].SKU)
        self.assertEqual(30000, request.items[1].price)
        self.assertEqual("P1M", request.period)
        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440001", str(request.requestInfo.requestReferenceId))
        self.assertEqual("taxCode", request.taxCode)
        self.assertEqual("USA", request.storefront)
        self.assertEqual("transactionId", request.previousTransactionId)

    def test_advanced_commerce_request_refund_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceRequestRefundRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceRequestRefundRequest).structure(request_dict, AdvancedCommerceRequestRefundRequest)

        self.assertEqual(2, len(request.items))
        self.assertEqual("sku", request.items[0].SKU)
        self.assertEqual(AdvancedCommerceRefundReason.LEGAL, request.items[0].refundReason)
        self.assertEqual(AdvancedCommerceRefundType.FULL, request.items[0].refundType)
        self.assertTrue(request.items[0].revoke)
        self.assertEqual("sku", request.items[1].SKU)
        self.assertEqual(AdvancedCommerceRefundReason.OTHER, request.items[1].refundReason)
        self.assertEqual(AdvancedCommerceRefundType.PRORATED, request.items[1].refundType)
        self.assertFalse(request.items[1].revoke)
        self.assertTrue(request.refundRiskingPreference)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440002", str(request.requestInfo.requestReferenceId))
        self.assertEqual("USD", request.currency)
        self.assertEqual("USA", request.storefront)
    
    def test_advanced_commerce_subscription_cancel_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCancelRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionCancelRequest).structure(request_dict, AdvancedCommerceSubscriptionCancelRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440003", str(request.requestInfo.requestReferenceId))
        self.assertEqual("USA", request.storefront)
    
    def test_advanced_commerce_subscription_revoke_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionRevokeRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionRevokeRequest).structure(request_dict, AdvancedCommerceSubscriptionRevokeRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440004", str(request.requestInfo.requestReferenceId))
        self.assertTrue(request.refundRiskingPreference)
        self.assertEqual("USA", request.storefront)
    
    def test_advanced_commerce_subscription_price_change_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionPriceChangeRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionPriceChangeRequest).structure(request_dict, AdvancedCommerceSubscriptionPriceChangeRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440005", str(request.requestInfo.requestReferenceId))
        self.assertEqual(1, len(request.items))
        self.assertEqual("sku123", request.items[0].SKU)
        self.assertEqual(15000, request.items[0].price)
        self.assertEqual("USD", request.currency)
    
    def test_advanced_commerce_request_refund_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceRequestRefundResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceRequestRefundResponse).structure(response_dict, AdvancedCommerceRequestRefundResponse)

        self.assertEqual("signed_transaction_info_value", response.signedTransactionInfo)

    def test_advanced_commerce_subscription_cancel_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCancelResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceSubscriptionCancelResponse).structure(response_dict, AdvancedCommerceSubscriptionCancelResponse)

        self.assertEqual("signed_renewal_info", response.signedRenewalInfo)
        self.assertEqual("signed_transaction_info", response.signedTransactionInfo)
    
    def test_advanced_commerce_subscription_revoke_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionRevokeResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceSubscriptionRevokeResponse).structure(response_dict, AdvancedCommerceSubscriptionRevokeResponse)

        self.assertEqual("signed_renewal_info", response.signedRenewalInfo)
        self.assertEqual("signed_transaction_info", response.signedTransactionInfo)

    def test_advanced_commerce_subscription_price_change_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionPriceChangeResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceSubscriptionPriceChangeResponse).structure(response_dict, AdvancedCommerceSubscriptionPriceChangeResponse)

        self.assertEqual("signed_renewal_info", response.signedRenewalInfo)
        self.assertEqual("signed_transaction_info", response.signedTransactionInfo)
    
    def test_advanced_commerce_subscription_change_metadata_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionChangeMetadataResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceSubscriptionChangeMetadataResponse).structure(response_dict, AdvancedCommerceSubscriptionChangeMetadataResponse)

        self.assertEqual("signed_renewal_info", response.signedRenewalInfo)
        self.assertEqual("signed_transaction_info", response.signedTransactionInfo)


    def test_advanced_commerce_subscription_migrate_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionMigrateRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionMigrateRequest).structure(request_dict, AdvancedCommerceSubscriptionMigrateRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440006", str(request.requestInfo.requestReferenceId))
        self.assertIsNotNone(request.descriptors)
        self.assertEqual("description", request.descriptors.description)
        self.assertEqual("display name", request.descriptors.displayName)
        self.assertEqual(1, len(request.items))
        self.assertEqual("sku", request.items[0].SKU)
        self.assertEqual("targetProductId", request.targetProductId)
        self.assertEqual("taxCode", request.taxCode)
    
    def test_advanced_commerce_subscription_modify_in_app_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyInAppRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyInAppRequest).structure(request_dict, AdvancedCommerceSubscriptionModifyInAppRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440007", str(request.requestInfo.requestReferenceId))
        self.assertEqual("transactionId", request.transactionId)
        self.assertTrue(request.retainBillingCycle)
        self.assertIsNotNone(request.descriptors)
        self.assertEqual("description", request.descriptors.description)
        self.assertEqual("display name", request.descriptors.displayName)
        self.assertEqual("taxCode", request.taxCode)
        self.assertEqual("USD", request.currency)
        
    def test_advanced_commerce_subscription_reactivate_in_app_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionReactivateInAppRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionReactivateInAppRequest).structure(request_dict, AdvancedCommerceSubscriptionReactivateInAppRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440008", str(request.requestInfo.requestReferenceId))
        self.assertEqual("transactionId", request.transactionId)
        self.assertEqual(1, len(request.items))
        self.assertEqual("sku", request.items[0].SKU)
    
    def test_advanced_commerce_subscription_change_metadata_request_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionChangeMetadataRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionChangeMetadataRequest).structure(request_dict, AdvancedCommerceSubscriptionChangeMetadataRequest)

        self.assertIsNotNone(request.requestInfo)
        self.assertEqual("550e8400-e29b-41d4-a716-446655440009", str(request.requestInfo.requestReferenceId))
        self.assertEqual(1, len(request.items))
        self.assertEqual("currentSKU", request.items[0].currentSKU)
        self.assertEqual("sku", request.items[0].SKU)
    
    def test_advanced_commerce_subscription_migrate_descriptors_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionMigrateDescriptors.json')

        descriptors_dict = json.loads(json_data)
        descriptors = _get_cattrs_converter(AdvancedCommerceSubscriptionMigrateDescriptors).structure(descriptors_dict, AdvancedCommerceSubscriptionMigrateDescriptors)

        self.assertEqual("description", descriptors.description)
        self.assertEqual("displayName", descriptors.displayName)
    
    def test_advanced_commerce_subscription_modify_descriptors_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyDescriptors.json')

        descriptors_dict = json.loads(json_data)
        descriptors = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyDescriptors).structure(descriptors_dict, AdvancedCommerceSubscriptionModifyDescriptors)

        self.assertEqual("description", descriptors.description)
        self.assertEqual("displayName", descriptors.displayName)
    
    def test_advanced_commerce_subscription_change_metadata_descriptors_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionChangeMetadataDescriptors.json')

        descriptors_dict = json.loads(json_data)
        descriptors = _get_cattrs_converter(AdvancedCommerceSubscriptionChangeMetadataDescriptors).structure(descriptors_dict, AdvancedCommerceSubscriptionChangeMetadataDescriptors)

        self.assertEqual("description", descriptors.description)
        self.assertEqual("displayName", descriptors.displayName)

    def test_advanced_commerce_subscription_change_metadata_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionChangeMetadataItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionChangeMetadataItem).structure(item_dict, AdvancedCommerceSubscriptionChangeMetadataItem)

        self.assertEqual("currentSku", item.currentSKU)
        self.assertEqual("sku", item.SKU)
        self.assertEqual("description", item.description)
        self.assertEqual("displayName", item.displayName)
    
    def test_advanced_commerce_subscription_migrate_renewal_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionMigrateRenewalItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionMigrateRenewalItem).structure(item_dict, AdvancedCommerceSubscriptionMigrateRenewalItem)

        self.assertEqual("sku", item.SKU)
        self.assertEqual("description", item.description)
        self.assertEqual("displayName", item.displayName)
    
    def test_advanced_commerce_subscription_modify_add_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyAddItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyAddItem).structure(item_dict, AdvancedCommerceSubscriptionModifyAddItem)

        self.assertEqual("sku", item.SKU)
        self.assertEqual("description", item.description)
        self.assertEqual("displayName", item.displayName)
        self.assertEqual(12000, item.price)
    
    def test_advanced_commerce_subscription_modify_change_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyChangeItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyChangeItem).structure(item_dict, AdvancedCommerceSubscriptionModifyChangeItem)

        self.assertEqual("currentSku", item.currentSKU)
        self.assertEqual("sku", item.SKU)
        self.assertEqual("description", item.description)
        self.assertEqual("displayName", item.displayName)
        self.assertEqual(13000, item.price)
    
    def test_advanced_commerce_subscription_modify_remove_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyRemoveItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyRemoveItem).structure(item_dict, AdvancedCommerceSubscriptionModifyRemoveItem)

        self.assertEqual("sku", item.SKU)
    
    def test_advanced_commerce_subscription_modify_period_change_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyPeriodChange.json')

        change_dict = json.loads(json_data)
        change = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyPeriodChange).structure(change_dict, AdvancedCommerceSubscriptionModifyPeriodChange)

        self.assertEqual("P3M", change.period)
    
    def test_advanced_commerce_subscription_price_change_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionPriceChangeItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionPriceChangeItem).structure(item_dict, AdvancedCommerceSubscriptionPriceChangeItem)

        self.assertEqual("sku", item.SKU)
        self.assertEqual(16000, item.price)
        self.assertEqual("dependentSKU", item.dependentSKUs[0])

    def test_advanced_commerce_subscription_price_change_item_dependent_sku_validation(self):
        valid_sku = "A" * 128
        too_long_sku = "A" * 129

        # Valid SKU in dependentSKUs is accepted
        item = AdvancedCommerceSubscriptionPriceChangeItem(SKU="sku", price=1000, dependentSKUs=[valid_sku])
        self.assertEqual(valid_sku, item.dependentSKUs[0])

        # Too-long SKU in dependentSKUs raises ValueError
        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionPriceChangeItem(SKU="sku", price=1000, dependentSKUs=[too_long_sku])

        # None list is allowed (field is optional)
        item_none = AdvancedCommerceSubscriptionPriceChangeItem(SKU="sku", price=1000, dependentSKUs=None)
        self.assertIsNone(item_none.dependentSKUs)

    def test_advanced_commerce_subscription_reactivate_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionReactivateItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionReactivateItem).structure(item_dict, AdvancedCommerceSubscriptionReactivateItem)

        self.assertEqual("sku", item.SKU)

    def test_advanced_commerce_request_info_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceRequestInfo.json')

        info_dict = json.loads(json_data)
        info = _get_cattrs_converter(AdvancedCommerceRequestInfo).structure(info_dict, AdvancedCommerceRequestInfo)

        self.assertEqual("550e8400-e29b-41d4-a716-446655440010", str(info.requestReferenceId))
        self.assertEqual("660e8400-e29b-41d4-a716-446655440011", str(info.appAccountToken))
        self.assertEqual("consistency_token_value", info.consistencyToken)

    def test_advanced_commerce_subscription_migrate_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionMigrateItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionMigrateItem).structure(item_dict, AdvancedCommerceSubscriptionMigrateItem)

        self.assertEqual("sku", item.SKU)
        self.assertEqual("description", item.description)
        self.assertEqual("displayName", item.displayName)

    def test_advanced_commerce_subscription_migrate_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionMigrateResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceSubscriptionMigrateResponse).structure(response_dict, AdvancedCommerceSubscriptionMigrateResponse)

        self.assertEqual("signed_renewal_info_value", response.signedRenewalInfo)
        self.assertEqual("signed_transaction_info_value", response.signedTransactionInfo)
