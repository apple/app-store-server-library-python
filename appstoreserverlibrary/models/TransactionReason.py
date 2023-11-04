# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum
from .LibraryUtility import AppStoreServerLibraryEnumMeta

class TransactionReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The cause of a purchase transaction, which indicates whether it’s a customer’s purchase or a renewal for an auto-renewable subscription that the system initiates.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionreason
    """
    PURCHASE = "PURCHASE"
    RENEWAL = "RENEWAL"
