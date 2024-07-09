# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class OfferType(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of subscription offer.
    
    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """
    INTRODUCTORY_OFFER = 1
    PROMOTIONAL_OFFER = 2
    SUBSCRIPTION_OFFER_CODE = 3
    WIN_BACK_OFFER = 4
