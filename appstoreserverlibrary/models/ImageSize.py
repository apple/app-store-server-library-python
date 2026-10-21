# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ImageSize(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The size of an image.

    https://developer.apple.com/documentation/retentionmessaging/imagesize
    """
    FULL_SIZE = "FULL_SIZE"
    """
    3840 pixels in width, and from 160 to 2160 pixels in height, inclusive.
    """

    BULLET_POINT = "BULLET_POINT"
    """
    1024 by 1024 pixels, to use for bullet points only.
    """
