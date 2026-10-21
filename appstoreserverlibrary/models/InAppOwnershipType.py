# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class InAppOwnershipType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A string that describes whether the transaction was purchased by the customer, or is available to them through Family Sharing, an organization, or a group.

    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """
    FAMILY_SHARED = "FAMILY_SHARED"
    """
    The transaction belongs to a family member who benefits from service.
    """

    PURCHASED = "PURCHASED"
    """
    The transaction belongs to the purchaser.
    """

    ASSIGNED = "ASSIGNED"
    """
    The transaction belongs to a customer who has access through an organization or group.
    """
