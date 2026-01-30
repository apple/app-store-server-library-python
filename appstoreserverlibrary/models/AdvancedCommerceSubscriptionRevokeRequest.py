# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from __future__ import annotations
from typing import Optional
import attr
from appstoreserverlibrary.models.AdvancedCommerceRequest import AdvancedCommerceRequest
from appstoreserverlibrary.models.AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from appstoreserverlibrary.models.AdvancedCommerceRefundType import AdvancedCommerceRefundType


@attr.define
class AdvancedCommerceSubscriptionRevokeRequest(AdvancedCommerceRequest):
    """
    The request body you provide to terminate a subscription and all its items immediately.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionrevokerequest
    """

    refundRiskingPreference: bool = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/refundriskingpreference
    """

    refundType: AdvancedCommerceRefundType = AdvancedCommerceRefundType.create_main_attr('rawRefundType', raw_required=True)

    rawRefundType: str = AdvancedCommerceRefundType.create_raw_attr('refundType', required=True)
    """
    See refundType
    """

    refundReason: AdvancedCommerceRefundReason = AdvancedCommerceRefundReason.create_main_attr('rawRefundReason', raw_required=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/refundreason
    """

    rawRefundReason: str = AdvancedCommerceRefundReason.create_raw_attr('refundReason', required=True)
    """
    See refundReason
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """