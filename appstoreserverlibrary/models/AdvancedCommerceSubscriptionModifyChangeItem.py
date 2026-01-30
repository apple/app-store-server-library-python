# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional
import attr
from attr import define
from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .AdvancedCommerceReason import AdvancedCommerceReason
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils


@define
class AdvancedCommerceSubscriptionModifyChangeItem(AbstractAdvancedCommerceItem):
    """
    The data your app provides to change an item of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifychangeitem
    """

    currentSKU: str = attr.ib(validator=AdvancedCommerceValidationUtils.sku_validator)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    price: int = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    reason: AdvancedCommerceReason = AdvancedCommerceReason.create_main_attr('rawReason', raw_required=True)

    rawReason: str = AdvancedCommerceReason.create_raw_attr('reason', required=True)
    """
    See reason
    """

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    proratedPrice: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/proratedprice
    """