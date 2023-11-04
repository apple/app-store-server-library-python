# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class UserStatus(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The status of a customer's account within your app.
    
    https://developer.apple.com/documentation/appstoreserverapi/userstatus
    """
    UNDECLARED = 0
    ACTIVE = 1
    SUSPENDED = 2
    TERMINATED = 3
    LIMITED_ACCESS = 4
