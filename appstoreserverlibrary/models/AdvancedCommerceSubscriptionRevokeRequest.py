# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from .AdvancedCommerceRefundType import AdvancedCommerceRefundType
from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionRevokeRequest(AdvancedCommerceRequest):
    """
    The request body you provide to terminate a subscription and all its items immediately.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionrevokerequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    refundReason: AdvancedCommerceRefundReason = AdvancedCommerceRefundReason.create_main_attr('rawRefundReason', raw_required=True, kw_only=True)
    """
    A reason to request a refund.

    https://developer.apple.com/documentation/advancedcommerceapi/refundreason
    """

    rawRefundReason: str = AdvancedCommerceRefundReason.create_raw_attr('refundReason', required=True)
    """
    See refundReason
    """

    refundRiskingPreference: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value that indicates whether the App Store asks you for consumption data to help inform the refund decision.

    https://developer.apple.com/documentation/advancedcommerceapi/refundriskingpreference
    """

    refundType: AdvancedCommerceRefundType = AdvancedCommerceRefundType.create_main_attr('rawRefundType', raw_required=True, kw_only=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionrevokerequest
    """

    rawRefundType: str = AdvancedCommerceRefundType.create_raw_attr('refundType', required=True)
    """
    See refundType
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
