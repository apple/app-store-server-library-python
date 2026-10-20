# Copyright (c) 2024 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ConsumptionRequestReason(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The customer-provided reason for a refund request.

    https://developer.apple.com/documentation/appstoreservernotifications/consumptionrequestreason
    """
    UNINTENDED_PURCHASE = "UNINTENDED_PURCHASE"
    """
    The customer didn’t intend to make the in-app purchase.
    """

    FULFILLMENT_ISSUE = "FULFILLMENT_ISSUE"
    """
    The customer had issues with receiving or using the in-app purchase.
    """

    UNSATISFIED_WITH_PURCHASE = "UNSATISFIED_WITH_PURCHASE"
    """
    The customer wasn’t satisfied with the in-app purchase.
    """

    LEGAL = "LEGAL"
    """
    The customer requested a refund based on a legal reason.
    """

    OTHER = "OTHER"
    """
    The customer requested a refund for other reasons.
    """
