# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceRefundReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A reason to request a refund.
    
    https://developer.apple.com/documentation/advancedcommerceapi/refundreason
    """
    
    UNINTENDED_PURCHASE = "UNINTENDED_PURCHASE"
    FULFILLMENT_ISSUE = "FULFILLMENT_ISSUE"
    UNSATISFIED_WITH_PURCHASE = "UNSATISFIED_WITH_PURCHASE"
    LEGAL = "LEGAL"
    OTHER = "OTHER"
    MODIFY_ITEMS_REFUND = "MODIFY_ITEMS_REFUND"
    SIMULATE_REFUND_DECLINE = "SIMULATE_REFUND_DECLINE"