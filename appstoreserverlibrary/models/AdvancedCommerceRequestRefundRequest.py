# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceRequestRefundItem import AdvancedCommerceRequestRefundItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceRequestRefundRequest(AdvancedCommerceRequest):
    """
    The request body for requesting a refund for a transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefundrequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    items: List[AdvancedCommerceRequestRefundItem] = attr.ib(kw_only=True, validator=HelperValidationUtils.items_validator)
    """
    Information about the refund request for an item, such as its SKU, the refund amount, reason, and type.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """

    refundRiskingPreference: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value that indicates whether the App Store asks you for consumption data to help inform the refund decision.

    https://developer.apple.com/documentation/advancedcommerceapi/refundriskingpreference
    """

    currency: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The currency of the transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
