# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem


@define
class AdvancedCommerceSubscriptionModifyRemoveItem(AbstractAdvancedCommerceBaseItem):
    """
    The data your app provides to remove an item from an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyremoveitem
    """