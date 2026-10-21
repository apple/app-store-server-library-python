# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import inspect
import json
from typing import Optional
import unittest
from uuid import UUID

import attr
from cattrs.errors import ClassValidationError

from appstoreserverlibrary.models.AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from appstoreserverlibrary.models.AdvancedCommerceEffective import AdvancedCommerceEffective
from appstoreserverlibrary.models.AdvancedCommerceOffer import AdvancedCommerceOffer
from appstoreserverlibrary.models.AdvancedCommerceOfferPeriod import AdvancedCommerceOfferPeriod
from appstoreserverlibrary.models.AdvancedCommerceOfferReason import AdvancedCommerceOfferReason
from appstoreserverlibrary.models.AdvancedCommerceOneTimeChargeCreateRequest import AdvancedCommerceOneTimeChargeCreateRequest
from appstoreserverlibrary.models.AdvancedCommerceOneTimeChargeItem import AdvancedCommerceOneTimeChargeItem
from appstoreserverlibrary.models.AdvancedCommercePeriod import AdvancedCommercePeriod
from appstoreserverlibrary.models.AdvancedCommercePriceIncreaseInfo import AdvancedCommercePriceIncreaseInfo
from appstoreserverlibrary.models.AdvancedCommercePriceIncreaseInfoStatus import AdvancedCommercePriceIncreaseInfoStatus
from appstoreserverlibrary.models.AdvancedCommerceReason import AdvancedCommerceReason
from appstoreserverlibrary.models.AdvancedCommerceRefund import AdvancedCommerceRefund
from appstoreserverlibrary.models.AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from appstoreserverlibrary.models.AdvancedCommerceRefundType import AdvancedCommerceRefundType
from appstoreserverlibrary.models.AdvancedCommerceRenewalInfo import AdvancedCommerceRenewalInfo
from appstoreserverlibrary.models.AdvancedCommerceRenewalItem import AdvancedCommerceRenewalItem
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
from appstoreserverlibrary.models.AdvancedCommerceTransactionInfo import AdvancedCommerceTransactionInfo
from appstoreserverlibrary.models.AdvancedCommerceTransactionItem import AdvancedCommerceTransactionItem
from appstoreserverlibrary.models.HelperValidationUtils import HelperValidationUtils
from appstoreserverlibrary.models.AutoRenewStatus import AutoRenewStatus
from appstoreserverlibrary.models.BillingPlanType import BillingPlanType
from appstoreserverlibrary.models.RenewalBillingPlanType import RenewalBillingPlanType
from appstoreserverlibrary.models.RenewalCommitmentInfo import RenewalCommitmentInfo
from appstoreserverlibrary.models.TransactionCommitmentInfo import TransactionCommitmentInfo
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter
from appstoreserverlibrary.signed_data_verifier import VerificationException, VerificationStatus
from tests.util import create_signed_data_from_dict, create_signed_data_from_json, get_default_signed_data_verifier, read_data_from_file


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
        HelperValidationUtils.description_validator(None, None, valid_description)

        max_length_description = "A" * 45
        HelperValidationUtils.description_validator(None, None, max_length_description)

        too_long_description = "A" * 46
        with self.assertRaises(ValueError):
            HelperValidationUtils.description_validator(None, None, too_long_description)

        with self.assertRaises(ValueError):
            HelperValidationUtils.description_validator(None, None, None)

    def test_validation_utils_display_name(self):
        valid_display_name = "Valid Name"
        HelperValidationUtils.display_name_validator(None, None, valid_display_name)

        max_length_display_name = "A" * 30
        HelperValidationUtils.display_name_validator(None, None, max_length_display_name)

        too_long_display_name = "A" * 31
        with self.assertRaises(ValueError):
            HelperValidationUtils.display_name_validator(None, None, too_long_display_name)

        with self.assertRaises(ValueError):
            HelperValidationUtils.display_name_validator(None, None, None)

    def test_validation_utils_sku(self):
        valid_sku = "valid.sku.123"
        HelperValidationUtils.sku_validator(None, None, valid_sku)

        max_length_sku = "A" * 128
        HelperValidationUtils.sku_validator(None, None, max_length_sku)

        too_long_sku = "A" * 129
        with self.assertRaises(ValueError):
            HelperValidationUtils.sku_validator(None, None, too_long_sku)

        with self.assertRaises(ValueError):
            HelperValidationUtils.sku_validator(None, None, None)

    def test_validation_utils_period_count(self):
        HelperValidationUtils.period_count_validator(None, None, 1)
        HelperValidationUtils.period_count_validator(None, None, 6)
        HelperValidationUtils.period_count_validator(None, None, 12)

        with self.assertRaises(ValueError):
            HelperValidationUtils.period_count_validator(None, None, 0)

        with self.assertRaises(ValueError):
            HelperValidationUtils.period_count_validator(None, None, 13)

        with self.assertRaises(ValueError):
            HelperValidationUtils.period_count_validator(None, None, None)

    def test_required_fields_reject_none(self):
        with self.assertRaises(ValueError):
            AdvancedCommerceDescriptors(description=None, displayName="name")

        with self.assertRaises(ValueError):
            AdvancedCommerceDescriptors(description="desc", displayName=None)

        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionCreateItem(SKU=None, description="desc", displayName="name", price=1000)

        with self.assertRaises(ValueError):
            AdvancedCommerceOffer(periodCount=None, price=1000, period=AdvancedCommerceOfferPeriod.P1M, reason=AdvancedCommerceOfferReason.ACQUISITION)

    def test_offer_rejects_non_integer_period_counts(self):
        for count in [1.5, 1.0, float('nan'), True, False, None, '1']:
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    AdvancedCommerceOffer(
                        periodCount=count, price=1000,
                        period=AdvancedCommerceOfferPeriod.P1M,
                        reason=AdvancedCommerceOfferReason.ACQUISITION
                    )

    def test_offer_accepts_integer_period_counts(self):
        for count in range(1, 13):
            with self.subTest(count=count):
                offer = AdvancedCommerceOffer(
                    periodCount=count, price=1000,
                    period=AdvancedCommerceOfferPeriod.P1M,
                    reason=AdvancedCommerceOfferReason.ACQUISITION
                )
                self.assertEqual(offer.periodCount, count)

    def test_validation_utils_items(self):
        valid_list = [
            AdvancedCommerceOneTimeChargeItem(
                description="desc",
                displayName="name",
                SKU="sku1",
                price=1000
            )
        ]
        HelperValidationUtils.items_validator(None, None, valid_list)

        with self.assertRaises(ValueError):
            HelperValidationUtils.items_validator(None, None, None)

        with self.assertRaises(ValueError):
            HelperValidationUtils.items_validator(None, None, [])

        list_with_none = [None]
        with self.assertRaises(ValueError):
            HelperValidationUtils.items_validator(None, None, list_with_none)

    def test_request_item_lists_are_validated(self):
        request_info = AdvancedCommerceRequestInfo(requestReferenceId=UUID("550e8400-e29b-41d4-a716-446655440000"))
        descriptors = AdvancedCommerceDescriptors(description="description", displayName="display name")
        create_item = AdvancedCommerceSubscriptionCreateItem(SKU="sku", description="description", displayName="display name", price=1000)
        for invalid_items in [[], [None], None]:
            with self.assertRaises(ValueError):
                AdvancedCommerceSubscriptionCreateRequest(requestInfo=request_info, currency="USD", descriptors=descriptors, items=invalid_items, taxCode="taxCode", period=AdvancedCommercePeriod.P1M)
            with self.assertRaises(ValueError):
                AdvancedCommerceSubscriptionPriceChangeRequest(requestInfo=request_info, items=invalid_items)
        for invalid_items in [[], [None]]:
            with self.assertRaises(ValueError):
                AdvancedCommerceSubscriptionModifyInAppRequest(requestInfo=request_info, transactionId="transactionId", retainBillingCycle=True, removeItems=invalid_items)

        AdvancedCommerceSubscriptionCreateRequest(requestInfo=request_info, currency="USD", descriptors=descriptors, items=[create_item], taxCode="taxCode", period=AdvancedCommercePeriod.P1M)
        AdvancedCommerceSubscriptionPriceChangeRequest(requestInfo=request_info, items=[AdvancedCommerceSubscriptionPriceChangeItem(SKU="sku", price=1000)])
        modify_request = AdvancedCommerceSubscriptionModifyInAppRequest(requestInfo=request_info, transactionId="transactionId", retainBillingCycle=True)
        self.assertIsNone(modify_request.removeItems)
        modify_request = AdvancedCommerceSubscriptionModifyInAppRequest(requestInfo=request_info, transactionId="transactionId", retainBillingCycle=True, removeItems=[AdvancedCommerceSubscriptionModifyRemoveItem(SKU="sku")])
        self.assertEqual(1, len(modify_request.removeItems))

    def test_reactivate_request_items_are_validated(self):
        request_info = AdvancedCommerceRequestInfo(requestReferenceId=UUID("550e8400-e29b-41d4-a716-446655440000"))
        item = AdvancedCommerceSubscriptionReactivateItem(SKU="sku")
        for invalid_items in [[], [None], [item, None]]:
            with self.assertRaises(ValueError):
                AdvancedCommerceSubscriptionReactivateInAppRequest(requestInfo=request_info, transactionId="transactionId", items=invalid_items)

        reactivate_request = AdvancedCommerceSubscriptionReactivateInAppRequest(requestInfo=request_info, transactionId="transactionId")
        self.assertIsNone(reactivate_request.items)
        with self.assertRaises(ValueError):
            reactivate_request.items = []

        reactivate_request = AdvancedCommerceSubscriptionReactivateInAppRequest(requestInfo=request_info, transactionId="transactionId", items=[item])
        self.assertEqual([item], reactivate_request.items)

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
        self.assertIsNone(response.signedRenewalInfo)

    def test_advanced_commerce_request_refund_response_with_signed_renewal_info_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceRequestRefundResponseWithSignedRenewalInfo.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceRequestRefundResponse).structure(response_dict, AdvancedCommerceRequestRefundResponse)

        self.assertEqual("signed_transaction_info_value", response.signedTransactionInfo)
        self.assertEqual("signed_renewal_info_value", response.signedRenewalInfo)
        self.assertEqual(AdvancedCommerceRequestRefundResponse(signedTransactionInfo="signed_transaction_info_value", signedRenewalInfo="signed_renewal_info_value"), response)

    def test_advanced_commerce_responses_reject_unknown_attributes(self):
        responses = [
            AdvancedCommerceRequestRefundResponse(signedTransactionInfo="signed_transaction_info"),
            AdvancedCommerceSubscriptionCancelResponse(signedRenewalInfo="signed_renewal_info", signedTransactionInfo="signed_transaction_info"),
            AdvancedCommerceSubscriptionChangeMetadataResponse(signedRenewalInfo="signed_renewal_info", signedTransactionInfo="signed_transaction_info"),
            AdvancedCommerceSubscriptionMigrateResponse(signedRenewalInfo="signed_renewal_info", signedTransactionInfo="signed_transaction_info"),
            AdvancedCommerceSubscriptionPriceChangeResponse(signedRenewalInfo="signed_renewal_info", signedTransactionInfo="signed_transaction_info"),
            AdvancedCommerceSubscriptionRevokeResponse(signedRenewalInfo="signed_renewal_info", signedTransactionInfo="signed_transaction_info"),
        ]
        for response in responses:
            with self.assertRaises(AttributeError):
                response.signedTransactionInf = "typo"

    def test_advanced_commerce_subscription_cancel_response_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCancelResponse.json')

        response_dict = json.loads(json_data)
        response = _get_cattrs_converter(AdvancedCommerceSubscriptionCancelResponse).structure(response_dict, AdvancedCommerceSubscriptionCancelResponse)

        self.assertEqual("signed_renewal_info", response.signedRenewalInfo)
        self.assertEqual("signed_transaction_info", response.signedTransactionInfo)
    
    def test_advanced_commerce_subscription_cancel_response_requires_documented_fields(self):
        with self.assertRaises(TypeError):
            AdvancedCommerceSubscriptionCancelResponse(signedTransactionInfo="signed_transaction_info")
        with self.assertRaises(TypeError):
            AdvancedCommerceSubscriptionCancelResponse(signedRenewalInfo="signed_renewal_info")

        c = _get_cattrs_converter(AdvancedCommerceSubscriptionCancelResponse)
        for field in ['signedRenewalInfo', 'signedTransactionInfo']:
            response_dict = json.loads(read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCancelResponse.json'))
            del response_dict[field]
            with self.subTest(field=field), self.assertRaises(ClassValidationError):
                c.structure(response_dict, AdvancedCommerceSubscriptionCancelResponse)

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

        self.assertEqual(AdvancedCommerceEffective.IMMEDIATELY, descriptors.effective)
        self.assertEqual("IMMEDIATELY", descriptors.rawEffective)
        self.assertEqual("description", descriptors.description)
        self.assertEqual("displayName", descriptors.displayName)
    
    def test_advanced_commerce_subscription_change_metadata_descriptors_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionChangeMetadataDescriptors.json')

        descriptors_dict = json.loads(json_data)
        descriptors = _get_cattrs_converter(AdvancedCommerceSubscriptionChangeMetadataDescriptors).structure(descriptors_dict, AdvancedCommerceSubscriptionChangeMetadataDescriptors)

        self.assertEqual(AdvancedCommerceEffective.IMMEDIATELY, descriptors.effective)
        self.assertEqual("IMMEDIATELY", descriptors.rawEffective)
        self.assertEqual("description", descriptors.description)
        self.assertEqual("displayName", descriptors.displayName)

    def test_advanced_commerce_subscription_change_metadata_item_deserialization(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionChangeMetadataItem.json')

        item_dict = json.loads(json_data)
        item = _get_cattrs_converter(AdvancedCommerceSubscriptionChangeMetadataItem).structure(item_dict, AdvancedCommerceSubscriptionChangeMetadataItem)

        self.assertEqual("currentSku", item.currentSKU)
        self.assertEqual(AdvancedCommerceEffective.NEXT_BILL_CYCLE, item.effective)
        self.assertEqual("NEXT_BILL_CYCLE", item.rawEffective)
        self.assertEqual("sku", item.SKU)
        self.assertEqual("description", item.description)
        self.assertEqual("displayName", item.displayName)
    
    def test_effective_is_set_from_raw_effective(self):
        change_metadata_descriptors = AdvancedCommerceSubscriptionChangeMetadataDescriptors(rawEffective="IMMEDIATELY")
        self.assertEqual(AdvancedCommerceEffective.IMMEDIATELY, change_metadata_descriptors.effective)
        self.assertEqual(AdvancedCommerceSubscriptionChangeMetadataDescriptors(effective=AdvancedCommerceEffective.IMMEDIATELY), change_metadata_descriptors)

        change_metadata_item = AdvancedCommerceSubscriptionChangeMetadataItem(currentSKU="sku", rawEffective="NEXT_BILL_CYCLE")
        self.assertEqual(AdvancedCommerceEffective.NEXT_BILL_CYCLE, change_metadata_item.effective)
        self.assertEqual(AdvancedCommerceSubscriptionChangeMetadataItem(currentSKU="sku", effective=AdvancedCommerceEffective.NEXT_BILL_CYCLE), change_metadata_item)

        modify_descriptors = AdvancedCommerceSubscriptionModifyDescriptors(rawEffective="IMMEDIATELY")
        self.assertEqual(AdvancedCommerceEffective.IMMEDIATELY, modify_descriptors.effective)
        self.assertEqual(AdvancedCommerceSubscriptionModifyDescriptors(effective=AdvancedCommerceEffective.IMMEDIATELY), modify_descriptors)

        unknown_effective = AdvancedCommerceSubscriptionModifyDescriptors(rawEffective="UNKNOWN")
        self.assertIsNone(unknown_effective.effective)
        self.assertEqual("UNKNOWN", unknown_effective.rawEffective)

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

        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionPriceChangeItem(SKU="sku", price=1000, dependentSKUs=[None])

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

    def test_one_time_charge_create_request_deserialization_sets_operation_and_version(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceOneTimeChargeCreateRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceOneTimeChargeCreateRequest).structure(request_dict, AdvancedCommerceOneTimeChargeCreateRequest)

        result = _get_cattrs_converter(AdvancedCommerceOneTimeChargeCreateRequest).unstructure(request)
        self.assertEqual("CREATE_ONE_TIME_CHARGE", result["operation"])
        self.assertEqual("1", result["version"])

    def test_subscription_create_request_deserialization_sets_operation_and_version(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionCreateRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionCreateRequest).structure(request_dict, AdvancedCommerceSubscriptionCreateRequest)

        result = _get_cattrs_converter(AdvancedCommerceSubscriptionCreateRequest).unstructure(request)
        self.assertEqual("CREATE_SUBSCRIPTION", result["operation"])
        self.assertEqual("1", result["version"])

    def test_subscription_modify_in_app_request_deserialization_sets_operation_and_version(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionModifyInAppRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyInAppRequest).structure(request_dict, AdvancedCommerceSubscriptionModifyInAppRequest)

        result = _get_cattrs_converter(AdvancedCommerceSubscriptionModifyInAppRequest).unstructure(request)
        self.assertEqual("MODIFY_SUBSCRIPTION", result["operation"])
        self.assertEqual("1", result["version"])

    def test_subscription_reactivate_in_app_request_deserialization_sets_operation_and_version(self):
        json_data = read_data_from_file('tests/resources/models/advancedCommerceSubscriptionReactivateInAppRequest.json')

        request_dict = json.loads(json_data)
        request = _get_cattrs_converter(AdvancedCommerceSubscriptionReactivateInAppRequest).structure(request_dict, AdvancedCommerceSubscriptionReactivateInAppRequest)

        result = _get_cattrs_converter(AdvancedCommerceSubscriptionReactivateInAppRequest).unstructure(request)
        self.assertEqual("REACTIVATE_SUBSCRIPTION", result["operation"])
        self.assertEqual("1", result["version"])

    def test_renewal_info_advanced_commerce_offer_decoding(self):
        signed_renewal_info = create_signed_data_from_json('tests/resources/models/signedRenewalInfoAdvancedCommerceOffer.json')

        renewal_info = get_default_signed_data_verifier().verify_and_decode_renewal_info(signed_renewal_info)

        ac_info = renewal_info.advancedCommerceInfo
        self.assertIsInstance(ac_info, AdvancedCommerceRenewalInfo)
        self.assertIsInstance(ac_info.descriptors, AdvancedCommerceDescriptors)
        self.assertEqual("Premium subscription, billed monthly", ac_info.descriptors.description)
        self.assertEqual("Premium", ac_info.descriptors.displayName)
        self.assertEqual(2, len(ac_info.items))
        self.assertIsInstance(ac_info.items[0], AdvancedCommerceRenewalItem)
        offer = ac_info.items[0].offer
        self.assertEqual(AdvancedCommerceOffer(periodCount=3, price=4990, period=AdvancedCommerceOfferPeriod.P1M, reason=AdvancedCommerceOfferReason.WIN_BACK), offer)
        self.assertEqual("P1M", offer.rawPeriod)
        self.assertEqual("WIN_BACK", offer.rawReason)
        offer = ac_info.items[1].offer
        self.assertIsInstance(offer, AdvancedCommerceOffer)
        self.assertIsNone(offer.period)
        self.assertEqual("P5Y", offer.rawPeriod)
        self.assertEqual(6, offer.periodCount)
        self.assertEqual(2990, offer.price)
        self.assertIsNone(offer.reason)
        self.assertEqual("NEW_REASON", offer.rawReason)

    def test_transaction_advanced_commerce_offer_decoding(self):
        signed_transaction = create_signed_data_from_json('tests/resources/models/signedTransactionAdvancedCommerceOffer.json')

        transaction = get_default_signed_data_verifier().verify_and_decode_transaction(signed_transaction)

        ac_info = transaction.advancedCommerceInfo
        self.assertIsInstance(ac_info, AdvancedCommerceTransactionInfo)
        self.assertIsInstance(ac_info.descriptors, AdvancedCommerceDescriptors)
        self.assertEqual("Premium Plan", ac_info.descriptors.description)
        self.assertEqual("Premium Plan Monthly", ac_info.descriptors.displayName)
        self.assertEqual(2, len(ac_info.items))
        self.assertIsInstance(ac_info.items[0], AdvancedCommerceTransactionItem)
        offer = ac_info.items[0].offer
        self.assertEqual(AdvancedCommerceOffer(periodCount=1, price=0, period=AdvancedCommerceOfferPeriod.P1W, reason=AdvancedCommerceOfferReason.ACQUISITION), offer)
        offer = ac_info.items[1].offer
        self.assertIsInstance(offer, AdvancedCommerceOffer)
        self.assertEqual(12, offer.periodCount)
        self.assertEqual(1990, offer.price)
        self.assertEqual(AdvancedCommerceOfferPeriod.P2W, offer.period)
        self.assertEqual("P2W", offer.rawPeriod)
        self.assertEqual(AdvancedCommerceOfferReason.RETENTION, offer.reason)
        self.assertEqual("RETENTION", offer.rawReason)

    def test_offer_or_descriptors_without_a_field_fail_to_decode_in_signed_data(self):
        verifier = get_default_signed_data_verifier()
        for path, decode in [('tests/resources/models/signedTransactionAdvancedCommerceOffer.json', verifier.verify_and_decode_transaction),
                             ('tests/resources/models/signedRenewalInfoAdvancedCommerceOffer.json', verifier.verify_and_decode_renewal_info)]:
            for obj, key in [('descriptors', 'displayName'), ('descriptors', 'description'),
                             ('offer', 'price'), ('offer', 'period'), ('offer', 'periodCount'), ('offer', 'reason')]:
                for missing in (True, False):
                    with self.subTest(path=path, field=f'{obj}.{key}', missing=missing):
                        payload = json.loads(read_data_from_file(path))
                        info = payload['advancedCommerceInfo']
                        target = info['descriptors'] if obj == 'descriptors' else info['items'][0]['offer']
                        if missing:
                            del target[key]
                        else:
                            target[key] = None
                        with self.assertRaises(VerificationException) as context:
                            decode(create_signed_data_from_dict(payload))
                        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_offer_or_descriptors_outside_the_request_limits_fail_to_decode_in_signed_data(self):
        verifier = get_default_signed_data_verifier()
        for path, decode in [('tests/resources/models/signedTransactionAdvancedCommerceOffer.json', verifier.verify_and_decode_transaction),
                             ('tests/resources/models/signedRenewalInfoAdvancedCommerceOffer.json', verifier.verify_and_decode_renewal_info)]:
            for obj, key, value in [('offer', 'periodCount', 13), ('offer', 'periodCount', 0),
                                    ('descriptors', 'displayName', 'A' * 31), ('descriptors', 'description', 'A' * 46)]:
                with self.subTest(path=path, field=f'{obj}.{key}', value=value):
                    payload = json.loads(read_data_from_file(path))
                    info = payload['advancedCommerceInfo']
                    target = info['descriptors'] if obj == 'descriptors' else info['items'][0]['offer']
                    target[key] = value
                    with self.assertRaises(VerificationException) as context:
                        decode(create_signed_data_from_dict(payload))
                    self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_offer_and_descriptors_at_the_request_limits_decode_in_signed_data(self):
        verifier = get_default_signed_data_verifier()
        for path, decode in [('tests/resources/models/signedTransactionAdvancedCommerceOffer.json', verifier.verify_and_decode_transaction),
                             ('tests/resources/models/signedRenewalInfoAdvancedCommerceOffer.json', verifier.verify_and_decode_renewal_info)]:
            for period_count in (1, 12):
                with self.subTest(path=path, periodCount=period_count):
                    payload = json.loads(read_data_from_file(path))
                    info = payload['advancedCommerceInfo']
                    info['descriptors']['displayName'] = 'A' * 30
                    info['descriptors']['description'] = 'B' * 45
                    info['items'][0]['offer']['periodCount'] = period_count

                    ac_info = decode(create_signed_data_from_dict(payload)).advancedCommerceInfo

                    self.assertEqual('A' * 30, ac_info.descriptors.displayName)
                    self.assertEqual('B' * 45, ac_info.descriptors.description)
                    self.assertEqual(period_count, ac_info.items[0].offer.periodCount)

    def test_one_time_charge_transaction_without_descriptors_or_offer_decodes(self):
        payload = json.loads(read_data_from_file('tests/resources/models/signedTransactionAdvancedCommerceOffer.json'))
        del payload['advancedCommerceInfo']['descriptors']
        del payload['advancedCommerceInfo']['period']
        del payload['advancedCommerceInfo']['items'][0]['offer']

        transaction = get_default_signed_data_verifier().verify_and_decode_transaction(create_signed_data_from_dict(payload))

        ac_info = transaction.advancedCommerceInfo
        self.assertIsNone(ac_info.descriptors)
        self.assertIsNone(ac_info.period)
        self.assertIsNone(ac_info.items[0].offer)
        self.assertEqual("com.example.sku.premium", ac_info.items[0].SKU)
        self.assertEqual(12, ac_info.items[1].offer.periodCount)

    def test_request_offer_and_descriptors_deserialization_is_still_validated(self):
        with self.assertRaises(ClassValidationError):
            _get_cattrs_converter(AdvancedCommerceOffer).structure({"period": "P1M", "periodCount": 13, "price": 4990, "reason": "WIN_BACK"}, AdvancedCommerceOffer)

        with self.assertRaises(ClassValidationError):
            _get_cattrs_converter(AdvancedCommerceDescriptors).structure({"description": "A" * 46, "displayName": "display name"}, AdvancedCommerceDescriptors)

        with self.assertRaises(ClassValidationError):
            _get_cattrs_converter(AdvancedCommerceSubscriptionCreateItem).structure({"SKU": "sku", "description": "description", "displayName": "display name", "price": 1000, "offer": {"period": "P1M", "periodCount": 0, "price": 0, "reason": "WIN_BACK"}}, AdvancedCommerceSubscriptionCreateItem)

    def test_advanced_commerce_price_increase_info_status(self):
        self.assertEqual("SCHEDULED", AdvancedCommercePriceIncreaseInfoStatus.SCHEDULED.value)
        self.assertEqual("PENDING", AdvancedCommercePriceIncreaseInfoStatus.PENDING.value)
        self.assertEqual("ACCEPTED", AdvancedCommercePriceIncreaseInfoStatus.ACCEPTED.value)

        self.assertEqual(AdvancedCommercePriceIncreaseInfoStatus.SCHEDULED,
            AdvancedCommercePriceIncreaseInfoStatus("SCHEDULED"))
        self.assertEqual(AdvancedCommercePriceIncreaseInfoStatus.PENDING,
            AdvancedCommercePriceIncreaseInfoStatus("PENDING"))
        self.assertEqual(AdvancedCommercePriceIncreaseInfoStatus.ACCEPTED,
            AdvancedCommercePriceIncreaseInfoStatus("ACCEPTED"))
        self.assertFalse("INVALID" in AdvancedCommercePriceIncreaseInfoStatus)

        self.assertEqual("SCHEDULED", AdvancedCommercePriceIncreaseInfoStatus.SCHEDULED.value)

    def test_billing_plan_type(self):
        self.assertEqual("BILLED_UPFRONT", BillingPlanType.BILLED_UPFRONT.value)
        self.assertEqual("MONTHLY", BillingPlanType.MONTHLY.value)

        self.assertEqual(BillingPlanType.BILLED_UPFRONT,
            BillingPlanType("BILLED_UPFRONT"))
        self.assertEqual(BillingPlanType.MONTHLY,
            BillingPlanType("MONTHLY"))
        self.assertFalse("INVALID" in BillingPlanType)

        self.assertEqual("MONTHLY", BillingPlanType.MONTHLY.value)

    def test_renewal_billing_plan_type(self):
        self.assertEqual("BILLED_UPFRONT", RenewalBillingPlanType.BILLED_UPFRONT.value)
        self.assertEqual("MONTHLY", RenewalBillingPlanType.MONTHLY.value)

        self.assertEqual(RenewalBillingPlanType.BILLED_UPFRONT,
            RenewalBillingPlanType("BILLED_UPFRONT"))
        self.assertEqual(RenewalBillingPlanType.MONTHLY,
            RenewalBillingPlanType("MONTHLY"))
        self.assertFalse("INVALID" in RenewalBillingPlanType)

        self.assertEqual("BILLED_UPFRONT", RenewalBillingPlanType.BILLED_UPFRONT.value)

    def test_transaction_commitment_info_billing_period_number_validation(self):
        info = TransactionCommitmentInfo(billingPeriodNumber=1)
        self.assertEqual(1, info.billingPeriodNumber)

        info = TransactionCommitmentInfo(billingPeriodNumber=12)
        self.assertEqual(12, info.billingPeriodNumber)

        info = TransactionCommitmentInfo(billingPeriodNumber=None)
        self.assertIsNone(info.billingPeriodNumber)

        for value in (0, 13, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                TransactionCommitmentInfo(billingPeriodNumber=value)

    def test_concrete_types_keep_the_inherited_attribute_order(self):
        expected = {
            AdvancedCommerceOneTimeChargeItem: ['SKU', 'description', 'displayName', 'price'],
            AdvancedCommerceSubscriptionCreateItem: ['SKU', 'description', 'displayName', 'price', 'offer'],
            AdvancedCommerceSubscriptionMigrateItem: ['SKU', 'description', 'displayName'],
            AdvancedCommerceSubscriptionMigrateRenewalItem: ['SKU', 'description', 'displayName'],
            AdvancedCommerceSubscriptionModifyAddItem: ['SKU', 'description', 'displayName', 'price', 'offer', 'proratedPrice'],
            AdvancedCommerceSubscriptionModifyChangeItem: ['SKU', 'description', 'displayName', 'currentSKU', 'effective', 'price', 'reason', 'offer', 'proratedPrice'],
            AdvancedCommerceRequestRefundItem: ['SKU', 'refundReason', 'refundType', 'revoke', 'refundAmount'],
            AdvancedCommerceSubscriptionModifyRemoveItem: ['SKU'],
            AdvancedCommerceSubscriptionPriceChangeItem: ['SKU', 'price', 'dependentSKUs'],
            AdvancedCommerceSubscriptionReactivateItem: ['SKU'],
            AdvancedCommerceSubscriptionMigrateDescriptors: ['description', 'displayName'],
            AdvancedCommerceOneTimeChargeCreateRequest: ['requestInfo', 'currency', 'item', 'taxCode', 'storefront'],
            AdvancedCommerceSubscriptionCreateRequest: ['requestInfo', 'currency', 'descriptors', 'items', 'period', 'taxCode', 'previousTransactionId', 'storefront'],
            AdvancedCommerceSubscriptionModifyInAppRequest: ['requestInfo', 'retainBillingCycle', 'transactionId', 'addItems', 'changeItems', 'currency', 'descriptors', 'periodChange', 'removeItems', 'storefront', 'taxCode'],
            AdvancedCommerceSubscriptionReactivateInAppRequest: ['requestInfo', 'transactionId', 'items', 'storefront'],
            AdvancedCommerceRequestRefundRequest: ['requestInfo', 'items', 'refundRiskingPreference', 'currency', 'storefront'],
            AdvancedCommerceSubscriptionCancelRequest: ['requestInfo', 'storefront'],
            AdvancedCommerceSubscriptionChangeMetadataRequest: ['requestInfo', 'descriptors', 'items', 'storefront', 'taxCode'],
            AdvancedCommerceSubscriptionMigrateRequest: ['requestInfo', 'descriptors', 'items', 'targetProductId', 'taxCode', 'renewalItems', 'storefront'],
            AdvancedCommerceSubscriptionPriceChangeRequest: ['requestInfo', 'items', 'currency', 'storefront'],
            AdvancedCommerceSubscriptionRevokeRequest: ['requestInfo', 'refundReason', 'refundRiskingPreference', 'refundType', 'storefront'],
        }
        validators = {
            'SKU': HelperValidationUtils.sku_validator,
            'description': HelperValidationUtils.description_validator,
            'displayName': HelperValidationUtils.display_name_validator,
        }
        for cls, order in expected.items():
            with self.subTest(cls=cls.__name__):
                parameters = inspect.signature(cls).parameters
                self.assertEqual(order, [name for name in parameters if not name.startswith('raw')])
                self.assertEqual([], [name for name, p in parameters.items() if p.kind != inspect.Parameter.KEYWORD_ONLY])
                cls_fields = attr.fields_dict(cls)
                for name, validator in validators.items():
                    if name in cls_fields:
                        self.assertIs(validator, cls_fields[name].validator)
                        self.assertIs(attr.NOTHING, cls_fields[name].default)
                if 'requestInfo' in cls_fields:
                    self.assertIs(attr.NOTHING, cls_fields['requestInfo'].default)

    def test_inherited_attributes_are_still_validated(self):
        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionModifyRemoveItem(SKU="a" * 129)
        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionReactivateItem(SKU=None)
        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionMigrateItem(SKU="sku", description="a" * 46, displayName="name")
        with self.assertRaises(ValueError):
            AdvancedCommerceSubscriptionMigrateDescriptors(description="description", displayName="a" * 31)
        with self.assertRaises(TypeError):
            AdvancedCommerceSubscriptionCancelRequest()

    def test_advanced_commerce_response_attribute_types(self):
        for cls in [AdvancedCommerceSubscriptionCancelResponse, AdvancedCommerceSubscriptionChangeMetadataResponse,
                    AdvancedCommerceSubscriptionMigrateResponse, AdvancedCommerceSubscriptionPriceChangeResponse,
                    AdvancedCommerceSubscriptionRevokeResponse]:
            with self.subTest(cls=cls.__name__):
                self.assertIs(str, attr.fields(cls).signedRenewalInfo.type)
                self.assertIs(str, attr.fields(cls).signedTransactionInfo.type)
                self.assertEqual(['signedRenewalInfo', 'signedTransactionInfo'], list(inspect.signature(cls).parameters))
        self.assertIs(str, attr.fields(AdvancedCommerceRequestRefundResponse).signedTransactionInfo.type)
        self.assertEqual(Optional[str], attr.fields(AdvancedCommerceRequestRefundResponse).signedRenewalInfo.type)
        parameters = inspect.signature(AdvancedCommerceRequestRefundResponse).parameters
        self.assertEqual(['signedTransactionInfo', 'signedRenewalInfo'], list(parameters))
        self.assertIsNone(parameters['signedRenewalInfo'].default)
        self.assertEqual(AdvancedCommerceRequestRefundResponse(signedTransactionInfo="transaction", signedRenewalInfo="renewal"),
                         AdvancedCommerceRequestRefundResponse(signedRenewalInfo="renewal", signedTransactionInfo="transaction"))

    def test_advanced_commerce_responses_reject_null_required_fields(self):
        cases = [
            (AdvancedCommerceRequestRefundResponse, 'advancedCommerceRequestRefundResponseWithSignedRenewalInfo.json', ['signedTransactionInfo']),
            (AdvancedCommerceSubscriptionCancelResponse, 'advancedCommerceSubscriptionCancelResponse.json', ['signedRenewalInfo', 'signedTransactionInfo']),
            (AdvancedCommerceSubscriptionChangeMetadataResponse, 'advancedCommerceSubscriptionChangeMetadataResponse.json', ['signedRenewalInfo', 'signedTransactionInfo']),
            (AdvancedCommerceSubscriptionMigrateResponse, 'advancedCommerceSubscriptionMigrateResponse.json', ['signedRenewalInfo', 'signedTransactionInfo']),
            (AdvancedCommerceSubscriptionPriceChangeResponse, 'advancedCommerceSubscriptionPriceChangeResponse.json', ['signedRenewalInfo', 'signedTransactionInfo']),
            (AdvancedCommerceSubscriptionRevokeResponse, 'advancedCommerceSubscriptionRevokeResponse.json', ['signedRenewalInfo', 'signedTransactionInfo']),
        ]
        for cls, file, fields in cases:
            c = _get_cattrs_converter(cls)
            for field in fields:
                response_dict = json.loads(read_data_from_file(f'tests/resources/models/{file}'))
                response_dict[field] = None
                with self.subTest(response=cls.__name__, field=field), self.assertRaises(ClassValidationError):
                    c.structure(response_dict, cls)

        response_dict = json.loads(read_data_from_file('tests/resources/models/advancedCommerceRequestRefundResponseWithSignedRenewalInfo.json'))
        response_dict['signedRenewalInfo'] = None
        response = _get_cattrs_converter(AdvancedCommerceRequestRefundResponse).structure(response_dict, AdvancedCommerceRequestRefundResponse)
        self.assertIsNone(response.signedRenewalInfo)

    def test_advanced_commerce_responses_reject_none_when_built(self):
        for cls in [AdvancedCommerceSubscriptionCancelResponse, AdvancedCommerceSubscriptionChangeMetadataResponse,
                    AdvancedCommerceSubscriptionMigrateResponse, AdvancedCommerceSubscriptionPriceChangeResponse,
                    AdvancedCommerceSubscriptionRevokeResponse]:
            for field in ['signedRenewalInfo', 'signedTransactionInfo']:
                values = dict(signedRenewalInfo="signed_renewal_info", signedTransactionInfo="signed_transaction_info")
                with self.subTest(response=cls.__name__, field=field):
                    with self.assertRaises(ValueError) as context:
                        cls(**dict(values, **{field: None}))
                    self.assertEqual(f'{field} cannot be None', str(context.exception))
                    response = cls(**values)
                    with self.assertRaises(ValueError):
                        setattr(response, field, None)
                    self.assertEqual(values[field], getattr(response, field))

        with self.assertRaises(ValueError):
            AdvancedCommerceRequestRefundResponse(signedTransactionInfo=None)
        self.assertIsNone(AdvancedCommerceRequestRefundResponse(signedTransactionInfo="signed_transaction_info", signedRenewalInfo=None).signedRenewalInfo)

    def test_advanced_commerce_requests_reject_none_when_built(self):
        request_info = AdvancedCommerceRequestInfo(requestReferenceId=UUID("550e8400-e29b-41d4-a716-446655440000"))
        with self.assertRaises(ValueError) as context:
            AdvancedCommerceRequestInfo(requestReferenceId=None)
        self.assertEqual('requestReferenceId cannot be None', str(context.exception))
        with self.assertRaises(ValueError) as context:
            AdvancedCommerceSubscriptionCancelRequest(requestInfo=None)
        self.assertEqual('requestInfo cannot be None', str(context.exception))
        with self.assertRaises(ValueError) as context:
            AdvancedCommerceOneTimeChargeItem(SKU="sku", description="description", displayName="display name", price=None)
        self.assertEqual('price cannot be None', str(context.exception))
        for field in ['transactionId', 'retainBillingCycle']:
            values = dict(requestInfo=request_info, transactionId="transactionId", retainBillingCycle=True)
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    AdvancedCommerceSubscriptionModifyInAppRequest(**dict(values, **{field: None}))
                request = AdvancedCommerceSubscriptionModifyInAppRequest(**values)
                with self.assertRaises(ValueError):
                    setattr(request, field, None)

    def test_offer_and_descriptors_types_are_required(self):
        offer_fields = attr.fields(AdvancedCommerceOffer)
        self.assertEqual(int, offer_fields.periodCount.type)
        self.assertEqual(int, offer_fields.price.type)
        self.assertEqual(AdvancedCommerceOfferPeriod, offer_fields.period.type)
        self.assertEqual(str, offer_fields.rawPeriod.type)
        self.assertEqual(AdvancedCommerceOfferReason, offer_fields.reason.type)
        self.assertEqual(str, offer_fields.rawReason.type)
        self.assertEqual(str, attr.fields(AdvancedCommerceDescriptors).description.type)
        self.assertEqual(str, attr.fields(AdvancedCommerceDescriptors).displayName.type)
        for cls, names in [(AdvancedCommerceOffer, ['periodCount', 'price']), (AdvancedCommerceDescriptors, ['description', 'displayName'])]:
            parameters = inspect.signature(cls).parameters
            for name in names:
                self.assertIs(inspect.Parameter.empty, parameters[name].default)
        with self.assertRaises(ValueError) as context:
            AdvancedCommerceOffer(periodCount=1, price=None, period=AdvancedCommerceOfferPeriod.P1M, reason=AdvancedCommerceOfferReason.ACQUISITION)
        self.assertEqual('price cannot be None', str(context.exception))

    def test_offer_and_descriptors_without_a_field_fail_to_decode(self):
        for cls, value in [(AdvancedCommerceOffer, {"period": "P1M", "periodCount": 3, "price": 4990, "reason": "WIN_BACK"}),
                           (AdvancedCommerceDescriptors, {"description": "description", "displayName": "display name"})]:
            converter = _get_cattrs_converter(cls)
            self.assertIsInstance(converter.structure(value, cls), cls)
            for key in value:
                with self.subTest(cls=cls.__name__, key=key):
                    with self.assertRaises(ClassValidationError):
                        converter.structure({k: v for k, v in value.items() if k != key}, cls)
                    with self.assertRaises(ClassValidationError):
                        converter.structure(dict(value, **{key: None}), cls)

    def test_offer_and_descriptors_are_required_to_build(self):
        with self.assertRaises(TypeError):
            AdvancedCommerceDescriptors(description="description")
        with self.assertRaises(TypeError):
            AdvancedCommerceDescriptors(displayName="display name")
        with self.assertRaises(TypeError):
            AdvancedCommerceOffer(price=1000, period=AdvancedCommerceOfferPeriod.P1M, reason=AdvancedCommerceOfferReason.ACQUISITION)
        with self.assertRaises(TypeError):
            AdvancedCommerceOffer(periodCount=1, period=AdvancedCommerceOfferPeriod.P1M, reason=AdvancedCommerceOfferReason.ACQUISITION)
        with self.assertRaises(ValueError):
            AdvancedCommerceOffer(periodCount=1, price=1000, reason=AdvancedCommerceOfferReason.ACQUISITION)
        with self.assertRaises(ValueError):
            AdvancedCommerceOffer(periodCount=1, price=1000, period=AdvancedCommerceOfferPeriod.P1M)
        with self.assertRaises(ValueError):
            AdvancedCommerceOffer(periodCount=13, price=1000, period=AdvancedCommerceOfferPeriod.P1M, reason=AdvancedCommerceOfferReason.ACQUISITION)
        with self.assertRaises(ValueError):
            AdvancedCommerceDescriptors(description="description", displayName="A" * 31)
