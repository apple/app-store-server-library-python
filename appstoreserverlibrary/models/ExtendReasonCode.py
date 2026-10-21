# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class ExtendReasonCode(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The code that represents the reason for the subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """
    UNDECLARED = 0
    """
    Undeclared; no information provided.
    """

    CUSTOMER_SATISFACTION = 1
    """
    The renewal-date extension is for customer satisfaction.
    """

    OTHER = 2
    """
    The renewal-date extension is for other reasons.
    """

    SERVICE_ISSUE_OR_OUTAGE = 3
    """
    The renewal-date extension is due to a service issue or outage.
    """
