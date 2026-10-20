# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class Role(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A string that identifies a customer’s role for a product within a group.

    https://developer.apple.com/documentation/appstoreserverapi/role
    """
    NONE = "NONE"
    """
    The customer has a seat in the group but doesn’t administer it.
    """

    ADMIN = "ADMIN"
    """
    The customer administers the group for the product.
    """
