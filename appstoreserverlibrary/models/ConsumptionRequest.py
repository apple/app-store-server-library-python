# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr
from .AccountTenure import AccountTenure

from .ConsumptionStatus import ConsumptionStatus
from .DeliveryStatus import DeliveryStatus
from .LifetimeDollarsPurchased import LifetimeDollarsPurchased
from .LifetimeDollarsRefunded import LifetimeDollarsRefunded
from .Platform import Platform
from .PlayTime import PlayTime
from .UserStatus import UserStatus

@define
class ConsumptionRequest: 
    """
    The request body containing consumption information.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequest
    """

    customerConsented: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether the customer consented to provide consumption data to the App Store.
    
    https://developer.apple.com/documentation/appstoreserverapi/customerconsented
    """

    consumptionStatus: Optional[ConsumptionStatus] = attr.ib(default=None)
    """
    A value that indicates the extent to which the customer consumed the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionstatus
    """

    platform: Optional[Platform] = attr.ib(default=None)
    """
    A value that indicates the platform on which the customer consumed the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/platform
    """

    sampleContentProvided: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether you provided, prior to its purchase, a free sample or trial of the content, or information about its functionality.
    
    https://developer.apple.com/documentation/appstoreserverapi/samplecontentprovided
    """

    deliveryStatus: Optional[DeliveryStatus] = attr.ib(default=None)
    """
    A value that indicates whether the app successfully delivered an in-app purchase that works properly.
    
    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """

    appAccountToken: Optional[str] = attr.ib(default=None)
    """
    The UUID that an app optionally generates to map a customer's in-app purchase with its resulting App Store transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """

    accountTenure: Optional[AccountTenure] = attr.ib(default=None)
    """
    The age of the customer's account.
    
    https://developer.apple.com/documentation/appstoreserverapi/accounttenure
    """

    playTime: Optional[PlayTime] = attr.ib(default=None)
    """
    A value that indicates the amount of time that the customer used the app.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequest
    """

    lifetimeDollarsRefunded: Optional[LifetimeDollarsRefunded] = attr.ib(default=None)
    """
    A value that indicates the total amount, in USD, of refunds the customer has received, in your app, across all platforms.
    
    https://developer.apple.com/documentation/appstoreserverapi/lifetimedollarsrefunded
    """

    lifetimeDollarsPurchased: Optional[LifetimeDollarsPurchased] = attr.ib(default=None)
    """
    A value that indicates the total amount, in USD, of in-app purchases the customer has made in your app, across all platforms.
    
    https://developer.apple.com/documentation/appstoreserverapi/lifetimedollarspurchased
    """

    userStatus: Optional[UserStatus] = attr.ib(default=None)
    """
    The status of the customer's account.
    
    https://developer.apple.com/documentation/appstoreserverapi/userstatus
    """