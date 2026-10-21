# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ExpirationIntent(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The reason an auto-renewable subscription expired.

    https://developer.apple.com/documentation/appstoreserverapi/expirationintent
    """
    CUSTOMER_CANCELLED = 1
    """
    The customer canceled their subscription.
    """

    BILLING_ERROR = 2
    """
    Billing error; for example, the customer’s payment information is no longer valid.
    """

    CUSTOMER_DID_NOT_CONSENT_TO_PRICE_INCREASE = 3
    """
    The customer didn’t consent to an auto-renewable subscription price increase that requires their consent, or to a subscription offer conversion that requires their consent, so the subscription expired.
    """

    PRODUCT_NOT_AVAILABLE = 4
    """
    The product wasn’t available for purchase at the time of renewal.
    """

    OTHER = 5
    """
    The subscription expired for some other reason.
    """
