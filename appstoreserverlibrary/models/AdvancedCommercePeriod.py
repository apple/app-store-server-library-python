# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommercePeriod(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The duration of a single cycle of an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/period
    """
    
    P1W = "P1W"
    P1M = "P1M"
    P2M = "P2M"
    P3M = "P3M"
    P6M = "P6M"
    P1Y = "P1Y"