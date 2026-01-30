# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceEffective(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A string value that indicates when a requested change to an auto-renewable subscription goes into effect.
    
    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """
    IMMEDIATELY = "IMMEDIATELY"
    NEXT_BILL_CYCLE = "NEXT_BILL_CYCLE"