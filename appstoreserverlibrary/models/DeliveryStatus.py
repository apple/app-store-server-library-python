# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class DeliveryStatus(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates whether the app successfully delivered an In-App Purchase that works properly.

    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """
    DELIVERED = "DELIVERED"
    """
    The app delivered the In-App Purchase and it’s working properly.
    """

    UNDELIVERED_QUALITY_ISSUE = "UNDELIVERED_QUALITY_ISSUE"
    """
    The app didn’t deliver the In-App Purchase due to a quality issue.
    """

    UNDELIVERED_WRONG_ITEM = "UNDELIVERED_WRONG_ITEM"
    """
    The app delivered the wrong item.
    """

    UNDELIVERED_SERVER_OUTAGE = "UNDELIVERED_SERVER_OUTAGE"
    """
    The app didn’t deliver the In-App Purchase due to a server outage.
    """

    UNDELIVERED_OTHER = "UNDELIVERED_OTHER"
    """
    The app didn’t deliver the In-App Purchase for other reasons.
    """
