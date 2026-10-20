# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class Subtype(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A string that provides details about select notification types in version 2.

    https://developer.apple.com/documentation/appstoreservernotifications/subtype
    """
    INITIAL_BUY = "INITIAL_BUY"
    """
    Applies to the SUBSCRIBED notificationType.
    """

    RESUBSCRIBE = "RESUBSCRIBE"
    """
    Applies to the SUBSCRIBED notificationType.
    """

    DOWNGRADE = "DOWNGRADE"
    """
    Applies to the DID_CHANGE_RENEWAL_PREF and OFFER_REDEEMED notificationType.
    """

    UPGRADE = "UPGRADE"
    """
    Applies to the DID_CHANGE_RENEWAL_PREF and OFFER_REDEEMED notificationType.
    """

    AUTO_RENEW_ENABLED = "AUTO_RENEW_ENABLED"
    """
    Applies to the DID_CHANGE_RENEWAL_STATUS notificationType.
    """

    AUTO_RENEW_DISABLED = "AUTO_RENEW_DISABLED"
    """
    Applies to the DID_CHANGE_RENEWAL_STATUS notificationType.
    """

    VOLUNTARY = "VOLUNTARY"
    """
    Applies to the EXPIRED notificationType.
    """

    BILLING_RETRY = "BILLING_RETRY"
    """
    Applies to the EXPIRED notificationType.
    """

    PRICE_INCREASE = "PRICE_INCREASE"
    """
    Applies to the EXPIRED notificationType.
    """

    GRACE_PERIOD = "GRACE_PERIOD"
    """
    Applies to the DID_FAIL_TO_RENEW notificationType.
    """

    PENDING = "PENDING"
    """
    Applies to the PRICE_INCREASE notificationType.
    """

    ACCEPTED = "ACCEPTED"
    """
    Applies to the PRICE_INCREASE notificationType.
    """

    BILLING_RECOVERY = "BILLING_RECOVERY"
    """
    Applies to the DID_RENEW notificationType.
    """

    PRODUCT_NOT_FOR_SALE = "PRODUCT_NOT_FOR_SALE"
    """
    Applies to the EXPIRED notificationType.
    """

    SUMMARY = "SUMMARY"
    """
    Applies to the RENEWAL_EXTENSION notificationType.
    """

    FAILURE = "FAILURE"
    """
    Applies to the RENEWAL_EXTENSION notificationType.
    """

    UNREPORTED = "UNREPORTED"
    """
    Applies to the EXTERNAL_PURCHASE_TOKEN notificationType.
    """

    CREATED = "CREATED"
    """
    Applies to the EXTERNAL_PURCHASE_TOKEN notificationType.
    """

    ACTIVE_TOKEN_REMINDER = "ACTIVE_TOKEN_REMINDER"
    """
    Applies to the EXTERNAL_PURCHASE_TOKEN notificationType.
    """
