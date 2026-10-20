# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class OrderLookupStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates whether the order ID in the request is valid for your app.

    https://developer.apple.com/documentation/appstoreserverapi/orderlookupstatus
    """
    VALID = 0
    """
    The orderId that you provided in the Look Up Order ID request is valid and contains at least one in-app purchase for your app.
    """

    INVALID = 1
    """
    The orderId is invalid or doesn’t contain any in-app purchases for your app.
    """
