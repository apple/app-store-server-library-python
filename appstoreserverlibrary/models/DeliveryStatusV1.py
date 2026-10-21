# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class DeliveryStatusV1(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates whether the app successfully delivered an In-App Purchase that works properly.

    .. deprecated:: 3.0.0
        Use :class:`DeliveryStatus` instead.

    https://developer.apple.com/documentation/appstoreserverapi/deliverystatusv1
    """
    DELIVERED_AND_WORKING_PROPERLY = 0
    """
    The app delivered the consumable In-App Purchase and it’s working properly.
    """

    DID_NOT_DELIVER_DUE_TO_QUALITY_ISSUE = 1
    """
    The app didn’t deliver the consumable In-App Purchase due to a quality issue.
    """

    DELIVERED_WRONG_ITEM = 2
    """
    The app delivered the wrong item.
    """

    DID_NOT_DELIVER_DUE_TO_SERVER_OUTAGE = 3
    """
    The app didn’t deliver the consumable In-App Purchase due to a server outage.
    """

    DID_NOT_DELIVER_DUE_TO_IN_GAME_CURRENCY_CHANGE = 4
    """
    The app didn’t deliver the consumable In-App Purchase due to an in-game currency change.
    """

    DID_NOT_DELIVER_FOR_OTHER_REASON = 5
    """
    The app didn’t deliver the consumable In-App Purchase for other reasons.
    """
