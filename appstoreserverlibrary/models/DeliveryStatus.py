# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class DeliveryStatus(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates whether the app successfully delivered an in-app purchase that works properly.

    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """
    DELIVERED = "DELIVERED"
    UNDELIVERED_QUALITY_ISSUE = "UNDELIVERED_QUALITY_ISSUE"
    UNDELIVERED_WRONG_ITEM = "UNDELIVERED_WRONG_ITEM"
    UNDELIVERED_SERVER_OUTAGE = "UNDELIVERED_SERVER_OUTAGE"
    UNDELIVERED_OTHER = "UNDELIVERED_OTHER"
