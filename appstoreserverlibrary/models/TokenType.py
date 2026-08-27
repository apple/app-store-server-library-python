# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class TokenType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of an external purchase custom link token.

    https://developer.apple.com/documentation/appstoreservernotifications/tokentype
    """
    SERVICES = "SERVICES"
    ACQUISITION = "ACQUISITION"
