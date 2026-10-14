# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class TokenType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of an external purchase custom link token.

    https://developer.apple.com/documentation/appstoreservernotifications/tokentype
    """
    ACQUISITION = "ACQUISITION"
    """
    A token type that indicates an initial acquisition.
    """

    SERVICES = "SERVICES"
    """
    A token type that indicates usage of App Store services.
    """

    CORE_TECHNOLOGY = "CORE_TECHNOLOGY"
    """
    A token type an app receives from the MarketplaceKit token(for:) API.
    """
