# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AdvancedCommerceRefundReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A reason to request a refund.

    https://developer.apple.com/documentation/advancedcommerceapi/refundreason
    """
    UNINTENDED_PURCHASE = "UNINTENDED_PURCHASE"
    """
    The customer didn’t intend to make the Apple In-App Purchase.
    """

    FULFILLMENT_ISSUE = "FULFILLMENT_ISSUE"
    """
    The customer had issues with receiving or using the Apple In-App Purchase.
    """

    UNSATISFIED_WITH_PURCHASE = "UNSATISFIED_WITH_PURCHASE"
    """
    The customer wasn’t satisfied with the Apple In-App Purchase.
    """

    LEGAL = "LEGAL"
    """
    The customer requested a refund based on a legal reason.
    """

    OTHER = "OTHER"
    """
    The customer requested a refund for other reasons.
    """

    MODIFY_ITEMS_REFUND = "MODIFY_ITEMS_REFUND"
    """
    The customer modified one or more items in the subscription, which results in a refund.
    """

    SIMULATE_REFUND_DECLINE = "SIMULATE_REFUND_DECLINE"
    """
    For testing purposes only, a simulation of a refund that the App Store declines.
    """
