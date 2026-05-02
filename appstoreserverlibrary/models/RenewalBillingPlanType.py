# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RenewalBillingPlanType(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    https://developer.apple.com/documentation/appstoreserverapi/renewalbillingplantype
    """
    BILLED_UPFRONT = "BILLED_UPFRONT"
    MONTHLY = "MONTHLY"
