# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class OfferDiscountType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The payment mode for a discount offer on an In-App Purchase.

    https://developer.apple.com/documentation/appstoreserverapi/offerdiscounttype
    """
    FREE_TRIAL = "FREE_TRIAL"
    """
    A payment mode of a discount for auto-renewable subscriptions that indicates a free trial.
    """

    PAY_AS_YOU_GO = "PAY_AS_YOU_GO"
    """
    A payment mode of a discount for auto-renewable subscriptions that customers pay over a single or multiple billing periods.
    """

    PAY_UP_FRONT = "PAY_UP_FRONT"
    """
    A payment mode of a discount for auto-renewable subscriptions that customers pay up front.
    """

    ONE_TIME = "ONE_TIME"
    """
    A payment mode for a discount for In-App Purchase types including consumable, non-consumable, and non-renewing subscription.
    """
