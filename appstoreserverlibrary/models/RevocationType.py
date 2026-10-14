# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RevocationType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The type of the refund or revocation that applies to the transaction.

    https://developer.apple.com/documentation/appstoreserverapi/revocationtype
    """
    REFUND_FULL = "REFUND_FULL"
    """
    The transaction has a full refund.
    """

    REFUND_PRORATED = "REFUND_PRORATED"
    """
    The transaction has a prorated refund.
    """

    FAMILY_REVOKE = "FAMILY_REVOKE"
    """
    The transaction is revoked from Family Sharing.
    """

    ASSIGNMENT_REVOKE = "ASSIGNMENT_REVOKE"
    """
    The organization or group purchaser removed the subscription from the customer.
    """
