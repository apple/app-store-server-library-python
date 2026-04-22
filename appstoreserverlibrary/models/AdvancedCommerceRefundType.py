# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceRefundType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    Information about the refund request for an item, such as its SKU, the refund amount, reason, and type.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """
    FULL = "FULL"
    PRORATED = "PRORATED"
    CUSTOM = "CUSTOM"