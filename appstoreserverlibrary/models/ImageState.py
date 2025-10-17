# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum
from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ImageState(Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The approval state of an image.

    https://developer.apple.com/documentation/retentionmessaging/imagestate
    """

    PENDING = "PENDING"
    """
    The image is awaiting approval.
    """

    APPROVED = "APPROVED"
    """
    The image is approved.
    """

    REJECTED = "REJECTED"
    """
    The image is rejected.
    """
