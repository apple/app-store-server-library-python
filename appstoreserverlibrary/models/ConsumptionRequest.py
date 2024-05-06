# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .AccountTenure import AccountTenure
from .ConsumptionStatus import ConsumptionStatus
from .DeliveryStatus import DeliveryStatus
from .LibraryUtility import AttrsRawValueAware
from .LifetimeDollarsPurchased import LifetimeDollarsPurchased
from .LifetimeDollarsRefunded import LifetimeDollarsRefunded
from .Platform import Platform
from .PlayTime import PlayTime
from .RefundPreference import RefundPreference
from .UserStatus import UserStatus

@define
class ConsumptionRequest(AttrsRawValueAware):
    """
    The request body containing consumption information.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequest
    """

    customerConsented: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether the customer consented to provide consumption data to the App Store.
    
    https://developer.apple.com/documentation/appstoreserverapi/customerconsented
    """

    consumptionStatus: Optional[ConsumptionStatus] = ConsumptionStatus.create_main_attr('rawConsumptionStatus')
    """
    A value that indicates the extent to which the customer consumed the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionstatus
    """

    rawConsumptionStatus: Optional[int] = ConsumptionStatus.create_raw_attr('consumptionStatus')
    """
    See consumptionStatus
    """

    platform: Optional[Platform] = Platform.create_main_attr('rawPlatform')
    """
    A value that indicates the platform on which the customer consumed the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/platform
    """

    rawPlatform: Optional[int] = Platform.create_raw_attr('platform')
    """
    See platform
    """

    sampleContentProvided: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether you provided, prior to its purchase, a free sample or trial of the content, or information about its functionality.
    
    https://developer.apple.com/documentation/appstoreserverapi/samplecontentprovided
    """

    deliveryStatus: Optional[DeliveryStatus] = DeliveryStatus.create_main_attr('rawDeliveryStatus')
    """
    A value that indicates whether the app successfully delivered an in-app purchase that works properly.
    
    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """

    rawDeliveryStatus: Optional[int] = DeliveryStatus.create_raw_attr('deliveryStatus')
    """
    See deliveryStatus
    """

    appAccountToken: Optional[str] = attr.ib(default=None)
    """
    The UUID that an app optionally generates to map a customer's in-app purchase with its resulting App Store transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """

    accountTenure: Optional[AccountTenure] = AccountTenure.create_main_attr('rawAccountTenure')
    """
    The age of the customer's account.
    
    https://developer.apple.com/documentation/appstoreserverapi/accounttenure
    """

    rawAccountTenure: Optional[int] = AccountTenure.create_raw_attr('accountTenure')
    """
    See accountTenure
    """

    playTime: Optional[PlayTime] = PlayTime.create_main_attr('rawPlayTime')
    """
    A value that indicates the amount of time that the customer used the app.
    
    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequest
    """

    rawPlayTime: Optional[int] = PlayTime.create_raw_attr('playTime')
    """
    See playTime
    """

    lifetimeDollarsRefunded: Optional[LifetimeDollarsRefunded] = LifetimeDollarsRefunded.create_main_attr('rawLifetimeDollarsRefunded')
    """
    A value that indicates the total amount, in USD, of refunds the customer has received, in your app, across all platforms.
    
    https://developer.apple.com/documentation/appstoreserverapi/lifetimedollarsrefunded
    """

    rawLifetimeDollarsRefunded: Optional[int] = LifetimeDollarsRefunded.create_raw_attr('lifetimeDollarsRefunded')
    """
    See lifetimeDollarsRefunded
    """

    lifetimeDollarsPurchased: Optional[LifetimeDollarsPurchased] = LifetimeDollarsPurchased.create_main_attr('rawLifetimeDollarsPurchased')
    """
    A value that indicates the total amount, in USD, of in-app purchases the customer has made in your app, across all platforms.
    
    https://developer.apple.com/documentation/appstoreserverapi/lifetimedollarspurchased
    """

    rawLifetimeDollarsPurchased: Optional[int] = LifetimeDollarsPurchased.create_raw_attr('lifetimeDollarsPurchased')
    """
    See lifetimeDollarsPurchased
    """

    userStatus: Optional[UserStatus] =  UserStatus.create_main_attr('rawUserStatus')
    """
    The status of the customer's account.
    
    https://developer.apple.com/documentation/appstoreserverapi/userstatus
    """

    rawUserStatus: Optional[int] = UserStatus.create_raw_attr('userStatus')
    """
    See userStatus
    """

    refundPreference: Optional[RefundPreference] =  RefundPreference.create_main_attr('rawRefundPreference')
    """
    A value that indicates your preference, based on your operational logic, as to whether Apple should grant the refund.
    
    https://developer.apple.com/documentation/appstoreserverapi/refundpreference
    """

    rawRefundPreference: Optional[int] = RefundPreference.create_raw_attr('refundPreference')
    """
    See refundPreference
    """