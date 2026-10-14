# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class Status(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The status of an auto-renewable subscription.

    https://developer.apple.com/documentation/appstoreserverapi/status
    """
    ACTIVE = 1
    """
    The auto-renewable subscription is active.
    """

    EXPIRED = 2
    """
    The auto-renewable subscription is expired.
    """

    BILLING_RETRY = 3
    """
    The auto-renewable subscription is in a billing retry period.
    """

    BILLING_GRACE_PERIOD = 4
    """
    The auto-renewable subscription is in a Billing Grace Period.
    """

    REVOKED = 5
    """
    The auto-renewable subscription is revoked.
    """
