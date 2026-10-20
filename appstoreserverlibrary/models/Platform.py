# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class Platform(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The platform on which the customer consumed the in-app purchase.

    https://developer.apple.com/documentation/appstoreserverapi/platform
    """
    UNDECLARED = 0
    """
    The platform is undeclared.
    """

    APPLE = 1
    """
    An Apple platform.
    """

    NON_APPLE = 2
    """
    Non-Apple platform.
    """
