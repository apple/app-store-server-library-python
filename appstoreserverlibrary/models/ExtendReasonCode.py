# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ExtendReasonCode(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The code that represents the reason for the subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """
    UNDECLARED = 0
    CUSTOMER_SATISFACTION = 1
    OTHER = 2
    SERVICE_ISSUE_OR_OUTAGE = 3
