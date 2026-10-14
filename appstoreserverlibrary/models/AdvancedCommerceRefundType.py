# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceRefundType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of refund requested.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """
    FULL = "FULL"
    PRORATED = "PRORATED"
    CUSTOM = "CUSTOM"
