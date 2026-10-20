# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .AccountTenure import AccountTenure
from .ConsumptionStatus import ConsumptionStatus
from .DeliveryStatusV1 import DeliveryStatusV1
from .LibraryUtility import AttrsRawValueAware, metadata_none_value_key, validate_not_none
from .LifetimeDollarsPurchased import LifetimeDollarsPurchased
from .LifetimeDollarsRefunded import LifetimeDollarsRefunded
from .Platform import Platform
from .PlayTime import PlayTime
from .RefundPreferenceV1 import RefundPreferenceV1
from .UserStatus import UserStatus

@define
class ConsumptionRequestV1(AttrsRawValueAware):
    """
    The request body containing consumption information.

    .. deprecated:: 3.0.0
        Use :class:`ConsumptionRequest` instead.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequestv1
    """

    accountTenure: AccountTenure = AccountTenure.create_main_attr('rawAccountTenure', raw_required=True, kw_only=True)
    """
    The age of the customer’s account.

    https://developer.apple.com/documentation/appstoreserverapi/accounttenure
    """

    rawAccountTenure: int = AccountTenure.create_raw_attr('accountTenure', required=True)
    """
    See accountTenure
    """

    appAccountToken: Optional[UUID] = attr.ib(kw_only=True, metadata={metadata_none_value_key: ''})
    """
    The UUID of the in-app user account that completed the in-app purchase transaction.

    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """

    consumptionStatus: ConsumptionStatus = ConsumptionStatus.create_main_attr('rawConsumptionStatus', raw_required=True, kw_only=True)
    """
    A value that indicates the extent to which the customer consumed the in-app purchase.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionstatus
    """

    rawConsumptionStatus: int = ConsumptionStatus.create_raw_attr('consumptionStatus', required=True)
    """
    See consumptionStatus
    """

    customerConsented: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value of true or false that indicates whether the customer consented to provide consumption data.

    https://developer.apple.com/documentation/appstoreserverapi/customerconsented
    """

    deliveryStatus: DeliveryStatusV1 = DeliveryStatusV1.create_main_attr('rawDeliveryStatus', raw_required=True, kw_only=True)
    """
    A value that indicates whether the app successfully delivered an in-app purchase that works properly.

    https://developer.apple.com/documentation/appstoreserverapi/deliverystatusv1
    """

    rawDeliveryStatus: int = DeliveryStatusV1.create_raw_attr('deliveryStatus', required=True)
    """
    See deliveryStatus
    """

    lifetimeDollarsPurchased: LifetimeDollarsPurchased = LifetimeDollarsPurchased.create_main_attr('rawLifetimeDollarsPurchased', raw_required=True, kw_only=True)
    """
    A value that indicates the total amount, in USD, of in-app purchases the customer has made in your app, across all platforms.

    https://developer.apple.com/documentation/appstoreserverapi/lifetimedollarspurchased
    """

    rawLifetimeDollarsPurchased: int = LifetimeDollarsPurchased.create_raw_attr('lifetimeDollarsPurchased', required=True)
    """
    See lifetimeDollarsPurchased
    """

    lifetimeDollarsRefunded: LifetimeDollarsRefunded = LifetimeDollarsRefunded.create_main_attr('rawLifetimeDollarsRefunded', raw_required=True, kw_only=True)
    """
    A value that indicates the total amount, in USD, of refunds the customer has received, in your app, across all platforms.

    https://developer.apple.com/documentation/appstoreserverapi/lifetimedollarsrefunded
    """

    rawLifetimeDollarsRefunded: int = LifetimeDollarsRefunded.create_raw_attr('lifetimeDollarsRefunded', required=True)
    """
    See lifetimeDollarsRefunded
    """

    platform: Platform = Platform.create_main_attr('rawPlatform', raw_required=True, kw_only=True)
    """
    A value that indicates the platform on which the customer consumed the in-app purchase.

    https://developer.apple.com/documentation/appstoreserverapi/platform
    """

    rawPlatform: int = Platform.create_raw_attr('platform', required=True)
    """
    See platform
    """

    playTime: PlayTime = PlayTime.create_main_attr('rawPlayTime', raw_required=True, kw_only=True)
    """
    A value that indicates the amount of time that the customer used the app.

    https://developer.apple.com/documentation/appstoreserverapi/playtime
    """

    rawPlayTime: int = PlayTime.create_raw_attr('playTime', required=True)
    """
    See playTime
    """

    sampleContentProvided: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value of true or false that indicates whether you provided, prior to its purchase, a free sample or trial of the content, or information about its functionality.

    https://developer.apple.com/documentation/appstoreserverapi/samplecontentprovided
    """

    userStatus: UserStatus = UserStatus.create_main_attr('rawUserStatus', raw_required=True, kw_only=True)
    """
    The status of the customer’s account.

    https://developer.apple.com/documentation/appstoreserverapi/userstatus
    """

    rawUserStatus: int = UserStatus.create_raw_attr('userStatus', required=True)
    """
    See userStatus
    """

    refundPreference: Optional[RefundPreferenceV1] = RefundPreferenceV1.create_main_attr('rawRefundPreference', kw_only=True)
    """
    A value that indicates your preference, based on your operational logic, as to whether Apple should grant the refund.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreferencev1
    """

    rawRefundPreference: Optional[int] = RefundPreferenceV1.create_raw_attr('refundPreference')
    """
    See refundPreference
    """
