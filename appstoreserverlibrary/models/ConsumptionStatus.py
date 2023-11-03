# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ConsumptionStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates the extent to which the customer consumed the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionstatus
    """
    UNDECLARED = 0
    NOT_CONSUMED = 1
    PARTIALLY_CONSUMED = 2
    FULLY_CONSUMED = 3
