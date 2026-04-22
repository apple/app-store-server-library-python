# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceOfferReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The reason for the offer.
    
    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """
    ACQUISITION = "ACQUISITION"
    WIN_BACK = "WIN_BACK"
    RETENTION = "RETENTION"