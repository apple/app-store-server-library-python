# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RefundPreference(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates your preference, based on your operational logic, as to whether Apple should grant the refund.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreference
    """
    DECLINE = "DECLINE"
    GRANT_FULL = "GRANT_FULL"
    GRANT_PRORATED = "GRANT_PRORATED"
