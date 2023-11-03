# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ExpirationIntent(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The reason an auto-renewable subscription expired.
    
    https://developer.apple.com/documentation/appstoreserverapi/expirationintent
    """
    CUSTOMER_CANCELLED = 1
    BILLING_ERROR = 2
    CUSTOMER_DID_NOT_CONSENT_TO_PRICE_INCREASE = 3
    PRODUCT_NOT_AVAILABLE = 4
    OTHER = 5
