# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RevocationReason(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The reason for a refunded transaction.

    https://developer.apple.com/documentation/appstoreserverapi/revocationreason
    """
    REFUNDED_DUE_TO_ISSUE = 1
    """
    The App Store refunded the transaction on behalf of the customer due to an actual or perceived issue within your app.
    """

    REFUNDED_FOR_OTHER_REASON = 0
    """
    The App Store refunded the transaction on behalf of the customer for other reasons, for example, an accidental purchase.
    """
