# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class PurchasePlatform(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The platform on which a customer originally purchases an app.

    https://developer.apple.com/documentation/storekit/appstore/platform
    https://developer.apple.com/documentation/appstoreserverapi/originalplatform
    """
    MAC_OS = "macOS"
    IOS = "iOS"
    TV_OS = "tvOS"
    VISION_OS = "visionOS"
