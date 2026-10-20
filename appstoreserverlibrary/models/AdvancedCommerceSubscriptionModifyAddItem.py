# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionModifyAddItem(AbstractAdvancedCommerceItem):
    """
    The data your app provides to add items when it makes changes to an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyadditem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The product identifier of an Apple In-App Purchase product you manage in your own system.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    description: str = attr.ib(kw_only=True, validator=HelperValidationUtils.description_validator)
    """
    A string you provide that describes a SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(kw_only=True, validator=HelperValidationUtils.display_name_validator)
    """
    A string with a product name that you can localize and is suitable for display to customers.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """

    price: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A price, in milliunits of a currency, for an Advanced Commerce API SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None, kw_only=True)
    """
    A discount offer for an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    proratedPrice: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    A prorated price, in milliunits of a currency, for an Advanced Commerce API SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/proratedprice
    """
