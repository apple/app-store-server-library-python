# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestRefundItem import AdvancedCommerceRequestRefundItem
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils

@define
class AdvancedCommerceRequestRefundRequest(AdvancedCommerceRequest):
    """
    The request body for requesting a refund for a transaction.
    
    https://developer.apple.com/documentation/advancedcommerceapi/requestrefundrequest
    """

    items: List[AdvancedCommerceRequestRefundItem] = attr.ib(validator=AdvancedCommerceValidationUtils.items_validator)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """

    refundRiskingPreference: bool = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/refundriskingpreference
    """

    currency: Optional[str] = attr.ib(default=None)
    """
    The currency of the transaction.
    
    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """