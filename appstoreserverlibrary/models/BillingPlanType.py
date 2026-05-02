# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class BillingPlanType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    https://developer.apple.com/documentation/appstoreserverapi/billingplantype
    """
    BILLED_UPFRONT = "BILLED_UPFRONT"
    MONTHLY = "MONTHLY"
