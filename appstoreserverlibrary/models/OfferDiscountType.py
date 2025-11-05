# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class OfferDiscountType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The payment mode for a discount offer on an In-App Purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/offerdiscounttype
    """
    FREE_TRIAL = "FREE_TRIAL"
    PAY_AS_YOU_GO = "PAY_AS_YOU_GO"
    PAY_UP_FRONT = "PAY_UP_FRONT"
    ONE_TIME = "ONE_TIME"