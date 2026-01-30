# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from appstoreserverlibrary.models.AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem


@define
class AdvancedCommerceSubscriptionReactivateItem(AbstractAdvancedCommerceBaseItem):
    """
    An item in a subscription to reactive.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateitem
    """