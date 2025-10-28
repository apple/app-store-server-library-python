# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class MessageState(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The approval state of the message.

    https://developer.apple.com/documentation/retentionmessaging/messagestate
    """
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
