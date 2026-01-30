# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from .AdvancedCommerceDescriptors import AdvancedCommerceDescriptors


@define
class AdvancedCommerceSubscriptionMigrateDescriptors(AdvancedCommerceDescriptors):
    """
    The description and display name of the subscription to migrate to that you manage.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigratedescriptors
    """