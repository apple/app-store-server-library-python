# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List
import attr
from attr import define
from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceSubscriptionPriceChangeItem import AdvancedCommerceSubscriptionPriceChangeItem

@define
class AdvancedCommerceSubscriptionPriceChangeRequest(AdvancedCommerceRequest):
    """
    The request body you use to change the price of an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangerequest
    """

    items: List[AdvancedCommerceSubscriptionPriceChangeItem] = attr.ib()
    """
    An array that contains one or more SKUs and the changed price for each SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangeitem
    """

    currency: Optional[str] = attr.ib(default=None)
    """
    The currency of the prices.
    
    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    The App Store storefront of the subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """