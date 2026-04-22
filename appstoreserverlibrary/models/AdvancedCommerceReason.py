# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The data your app provides to change an item of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifychangeitem
    """
    UPGRADE = "UPGRADE"
    DOWNGRADE = "DOWNGRADE"
    APPLY_OFFER = "APPLY_OFFER"