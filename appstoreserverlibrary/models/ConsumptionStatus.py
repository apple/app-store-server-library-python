# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ConsumptionStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates the extent to which the customer consumed the In-App Purchase.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionstatus
    """
    UNDECLARED = 0
    """
    The consumption status is undeclared.
    """

    NOT_CONSUMED = 1
    """
    The In-App Purchase is not consumed.
    """

    PARTIALLY_CONSUMED = 2
    """
    The In-App Purchase is partially consumed.
    """

    FULLY_CONSUMED = 3
    """
    The In-App Purchase is fully consumed.
    """
