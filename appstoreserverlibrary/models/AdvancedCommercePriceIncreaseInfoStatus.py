# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommercePriceIncreaseInfoStatus(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    https://developer.apple.com/documentation/appstoreservernotifications/advancedcommercepriceincreaseinfostatus
    """
    SCHEDULED = "SCHEDULED"
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
