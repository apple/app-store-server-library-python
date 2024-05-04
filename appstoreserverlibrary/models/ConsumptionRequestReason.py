# Copyright (c) 2024 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ConsumptionRequestReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The customer-provided reason for a refund request.
    
    https://developer.apple.com/documentation/appstoreservernotifications/consumptionrequestreason
    """
    UNINTENDED_PURCHASE = "UNINTENDED_PURCHASE"
    FULFILLMENT_ISSUE = "FULFILLMENT_ISSUE"
    UNSATISFIED_WITH_PURCHASE = "UNSATISFIED_WITH_PURCHASE"
    LEGAL = "LEGAL"
    OTHER = "OTHER"
