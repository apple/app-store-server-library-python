# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AccountTenure(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The age of the customer’s account.

    https://developer.apple.com/documentation/appstoreserverapi/accounttenure
    """
    UNDECLARED = 0
    """
    Account age is undeclared.
    """

    ZERO_TO_THREE_DAYS = 1
    """
    Account age is between 0–3 days.
    """

    THREE_DAYS_TO_TEN_DAYS = 2
    """
    Account age is between 3–10 days.
    """

    TEN_DAYS_TO_THIRTY_DAYS = 3
    """
    Account age is between 10–30 days.
    """

    THIRTY_DAYS_TO_NINETY_DAYS = 4
    """
    Account age is between 30–90 days.
    """

    NINETY_DAYS_TO_ONE_HUNDRED_EIGHTY_DAYS = 5
    """
    Account age is between 90–180 days.
    """

    ONE_HUNDRED_EIGHTY_DAYS_TO_THREE_HUNDRED_SIXTY_FIVE_DAYS = 6
    """
    Account age is between 180–365 days.
    """

    GREATER_THAN_THREE_HUNDRED_SIXTY_FIVE_DAYS = 7
    """
    Account age is over 365 days.
    """
