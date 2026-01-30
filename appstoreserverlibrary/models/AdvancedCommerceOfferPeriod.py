# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceOfferPeriod(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The period of the offer.
    
    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """
    P3D = "P3D"
    P1W = "P1W"
    P2W = "P2W"
    P1M = "P1M"
    P2M = "P2M"
    P3M = "P3M"
    P6M = "P6M"
    P9M = "P9M"
    P1Y = "P1Y"