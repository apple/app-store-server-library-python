# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class HeaderPosition(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The position where the header text appears in a message.

    https://developer.apple.com/documentation/retentionmessaging/headerposition
    """
    ABOVE_BODY = "ABOVE_BODY"
    ABOVE_IMAGE = "ABOVE_IMAGE"
