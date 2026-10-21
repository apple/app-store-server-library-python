# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class GroupType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A string that describes the kind of multiseat purchase a customer’s access comes from.

    https://developer.apple.com/documentation/appstoreserverapi/grouptype
    """
    ORGANIZATION = "ORGANIZATION"
    """
    An organization bought seats through Volume Purchasing and assigned one to the customer.
    """

    CONSUMER = "CONSUMER"
    """
    A subscriber bought seats through Group Purchases and invited the customer to join.
    """
