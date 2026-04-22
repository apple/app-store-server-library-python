# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional
import attr
from attr import define
from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .AdvancedCommerceOffer import AdvancedCommerceOffer


@define
class AdvancedCommerceSubscriptionCreateItem(AbstractAdvancedCommerceItem):
    """
    The data that describes a subscription item.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreateitem
    """

    price: int = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """