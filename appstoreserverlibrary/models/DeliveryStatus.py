# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class DeliveryStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates whether the app successfully delivered an in-app purchase that works properly.
    
    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """
    DELIVERED_AND_WORKING_PROPERLY = 0
    DID_NOT_DELIVER_DUE_TO_QUALITY_ISSUE = 1
    DELIVERED_WRONG_ITEM = 2
    DID_NOT_DELIVER_DUE_TO_SERVER_OUTAGE = 3
    DID_NOT_DELIVER_DUE_TO_IN_GAME_CURRENCY_CHANGE = 4
    DID_NOT_DELIVER_FOR_OTHER_REASON = 5
