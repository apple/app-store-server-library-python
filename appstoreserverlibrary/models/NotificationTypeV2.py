# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

class NotificationTypeV2(Enum): 
    """
    A notification type value that App Store Server Notifications V2 uses.
    
    https://developer.apple.com/documentation/appstoreserverapi/notificationtype
    """
    SUBSCRIBED = "SUBSCRIBED"
    DID_CHANGE_RENEWAL_PREF = "DID_CHANGE_RENEWAL_PREF"
    DID_CHANGE_RENEWAL_STATUS = "DID_CHANGE_RENEWAL_STATUS"
    OFFER_REDEEMED = "OFFER_REDEEMED"
    DID_RENEW = "DID_RENEW"
    EXPIRED = "EXPIRED"
    DID_FAIL_TO_RENEW = "DID_FAIL_TO_RENEW"
    GRACE_PERIOD_EXPIRED = "GRACE_PERIOD_EXPIRED"
    PRICE_INCREASE = "PRICE_INCREASE"
    REFUND = "REFUND"
    REFUND_DECLINED = "REFUND_DECLINED"
    CONSUMPTION_REQUEST = "CONSUMPTION_REQUEST"
    RENEWAL_EXTENDED = "RENEWAL_EXTENDED"
    REVOKE = "REVOKE"
    TEST = "TEST"
    RENEWAL_EXTENSION = "RENEWAL_EXTENSION"
    REFUND_REVERSED = "REFUND_REVERSED"
