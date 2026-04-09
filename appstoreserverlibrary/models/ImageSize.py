# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ImageSize(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The size of an image.

    https://developer.apple.com/documentation/retentionmessaging/imagesize
    """
    FULL_SIZE = "FULL_SIZE"
    BULLET_POINT = "BULLET_POINT"
