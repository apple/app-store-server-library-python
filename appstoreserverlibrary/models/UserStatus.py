# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class UserStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The status of a customer’s account within your app.

    https://developer.apple.com/documentation/appstoreserverapi/userstatus
    """
    UNDECLARED = 0
    """
    Account status is undeclared.
    """

    ACTIVE = 1
    """
    The customer’s account is active.
    """

    SUSPENDED = 2
    """
    The customer’s account is suspended.
    """

    TERMINATED = 3
    """
    The customer’s account is terminated.
    """

    LIMITED_ACCESS = 4
    """
    The customer’s account has limited access.
    """
