# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RefundPreference(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates your preferred outcome for the refund request.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreference
    """
    DECLINE = "DECLINE"
    """
    You prefer that the App Store declines the refund.
    """

    GRANT_FULL = "GRANT_FULL"
    """
    You prefer that the App Store grants the refund in full.
    """

    GRANT_PRORATED = "GRANT_PRORATED"
    """
    You prefer that the App Store grants a prorated refund.
    """
