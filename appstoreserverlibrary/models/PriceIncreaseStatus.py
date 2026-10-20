# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class PriceIncreaseStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The status that indicates whether an auto-renewable subscription is subject to a price increase.

    https://developer.apple.com/documentation/appstoreserverapi/priceincreasestatus
    """
    CUSTOMER_HAS_NOT_RESPONDED = 0
    """
    The customer hasn’t yet responded to an auto-renewable subscription price increase that requires customer consent.
    """

    CUSTOMER_CONSENTED_OR_WAS_NOTIFIED_WITHOUT_NEEDING_CONSENT = 1
    """
    The customer consented to an auto-renewable subscription price increase that requires customer consent, or the App Store has notified the customer of an auto-renewable subscription price increase that doesn’t require consent.
    """
