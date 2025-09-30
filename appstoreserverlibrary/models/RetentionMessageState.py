# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum
from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RetentionMessageState(Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The approval state of the message.

    https://developer.apple.com/documentation/retentionmessaging/messagestate
    """

    PENDING = "PENDING"
    """
    The message is awaiting approval.
    """

    APPROVED = "APPROVED"
    """
    The message is approved.
    """

    REJECTED = "REJECTED"
    """
    The message is rejected.
    """