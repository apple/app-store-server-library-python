# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .AdvancedCommercePriceIncreaseInfo import AdvancedCommercePriceIncreaseInfo

@define
class AdvancedCommerceRenewalItem:
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerenewalitem
    """

    SKU: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercesku
    """

    description: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedescription
    """

    displayName: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedisplayname
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceoffer
    """

    price: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceprice
    """

    priceIncreaseInfo: Optional[AdvancedCommercePriceIncreaseInfo] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercepriceincreaseinfo
    """
