# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommercePeriod(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The duration of a single cycle of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/period
    """
    P1W = "P1W"
    """
    A period that is 1 week in duration.
    """

    P1M = "P1M"
    """
    A period that is 1 month in duration.
    """

    P2M = "P2M"
    """
    A period that is 2 months in duration.
    """

    P3M = "P3M"
    """
    A period that is 3 months in duration.
    """

    P6M = "P6M"
    """
    A period that is 6 months in duration.
    """

    P1Y = "P1Y"
    """
    A period that is 1 year in duration.
    """
