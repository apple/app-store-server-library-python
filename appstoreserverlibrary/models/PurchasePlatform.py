# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class PurchasePlatform(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    Values that represent Apple platforms.
    
    https://developer.apple.com/documentation/storekit/appstore/platform
    """
    IOS = "iOS"
    MAC_OS = "macOS"
    TV_OS = "tvOS"
    VISION_OS = "visionOS"
