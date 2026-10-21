# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .AdvancedCommerceReason import AdvancedCommerceReason
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionModifyChangeItem(AbstractAdvancedCommerceItem):
    """
    The data your app provides to change an item of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifychangeitem
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

    currentSKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The product identifier of an Apple In-App Purchase product you manage in your own system.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True, kw_only=True)
    """
    A string value that indicates when a requested change to an auto-renewable subscription goes into effect.

    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    price: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A price, in milliunits of a currency, for an Advanced Commerce API SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    reason: AdvancedCommerceReason = AdvancedCommerceReason.create_main_attr('rawReason', raw_required=True, kw_only=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifychangeitem
    """

    rawReason: str = AdvancedCommerceReason.create_raw_attr('reason', required=True)
    """
    See reason
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
