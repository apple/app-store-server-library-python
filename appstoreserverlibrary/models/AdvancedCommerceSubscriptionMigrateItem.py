# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem


@define
class AdvancedCommerceSubscriptionMigrateItem(AbstractAdvancedCommerceItem):
    """
    The SKU, description, and display name to use for a migrated subscription item.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigrateitem
    """