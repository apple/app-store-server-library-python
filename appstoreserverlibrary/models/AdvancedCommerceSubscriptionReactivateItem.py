# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionReactivateItem(AbstractAdvancedCommerceBaseItem):
    """
    An item in a subscription to reactivate.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The SKU of the item to reactivate.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """
