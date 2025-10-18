# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ImageState(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The approval state of an image.

    https://developer.apple.com/documentation/retentionmessaging/imagestate
    """
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
