# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class OfferType(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of offer.

    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """
    INTRODUCTORY_OFFER = 1
    """
    An introductory offer.
    """

    PROMOTIONAL_OFFER = 2
    """
    A promotional offer.
    """

    OFFER_CODE = 3
    """
    An offer with an offer code.
    """

    WIN_BACK_OFFER = 4
    """
    A win-back offer.
    """
