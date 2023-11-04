# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class PriceIncreaseStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The status that indicates whether an auto-renewable subscription is subject to a price increase.
    
    https://developer.apple.com/documentation/appstoreserverapi/priceincreasestatus
    """
    CUSTOMER_HAS_NOT_RESPONDED = 0
    CUSTOMER_CONSENTED_OR_WAS_NOTIFIED_WITHOUT_NEEDING_CONSENT = 1
