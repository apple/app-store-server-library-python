# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class AccountTenure(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The age of the customer's account.
    
    https://developer.apple.com/documentation/appstoreserverapi/accounttenure
    """
    UNDECLARED = 0
    ZERO_TO_THREE_DAYS = 1
    THREE_DAYS_TO_TEN_DAYS = 2
    TEN_DAYS_TO_THIRTY_DAYS = 3
    THIRTY_DAYS_TO_NINETY_DAYS = 4
    NINETY_DAYS_TO_ONE_HUNDRED_EIGHTY_DAYS = 5
    ONE_HUNDRED_EIGHTY_DAYS_TO_THREE_HUNDRED_SIXTY_FIVE_DAYS = 6
    GREATER_THAN_THREE_HUNDRED_SIXTY_FIVE_DAYS = 7
