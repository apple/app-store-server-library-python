# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionCreateItem(AbstractAdvancedCommerceItem):
    """
    The data that describes a subscription item.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreateitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The item’s product identifier, which you define.

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
