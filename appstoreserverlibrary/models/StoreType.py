# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class StoreType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A string that describes the store the customer obtained the app from.

    https://developer.apple.com/documentation/appstoreserverapi/storetype
    """
    CONSUMER = "CONSUMER"
    """
    The customer obtained the app from the App Store.
    """
