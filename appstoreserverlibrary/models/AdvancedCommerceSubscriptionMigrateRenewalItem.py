# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem


@define
class AdvancedCommerceSubscriptionMigrateRenewalItem(AbstractAdvancedCommerceItem):
    """
    The item information that replaces a migrated subscription item when the subscription renews.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigraterenewalitem
    """