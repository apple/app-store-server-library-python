# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionModifyRemoveItem(AbstractAdvancedCommerceBaseItem):
    """
    The data your app provides to remove an item from an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyremoveitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The product identifier of an Apple In-App Purchase product you manage in your own system.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """
