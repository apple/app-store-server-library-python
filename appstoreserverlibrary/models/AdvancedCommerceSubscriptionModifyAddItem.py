# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional
import attr
from attr import define
from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .AdvancedCommerceOffer import AdvancedCommerceOffer


@define
class AdvancedCommerceSubscriptionModifyAddItem(AbstractAdvancedCommerceItem):
    """
    The data your app provides to add items when it makes changes to an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyadditem
    """

    price: int = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None)
    """
    A discount offer for an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    proratedPrice: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/proratedprice
    """