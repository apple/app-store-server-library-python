# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RevocationType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of the refund or revocation that applies to the transaction.

    https://developer.apple.com/documentation/appstoreservernotifications/revocationtype
    """
    REFUND_FULL = "REFUND_FULL"
    REFUND_PRORATED = "REFUND_PRORATED"
    FAMILY_REVOKE = "FAMILY_REVOKE"
