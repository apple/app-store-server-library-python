# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class OfferDiscountType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The payment mode you configure for an introductory offer, promotional offer, or offer code on an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/offerdiscounttype
    """
    FREE_TRIAL = "FREE_TRIAL"
    PAY_AS_YOU_GO = "PAY_AS_YOU_GO"
    PAY_UP_FRONT = "PAY_UP_FRONT"