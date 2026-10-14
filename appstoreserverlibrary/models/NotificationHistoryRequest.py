# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware, validate_not_none
from .NotificationTypeV2 import NotificationTypeV2
from .Subtype import Subtype

@define
class NotificationHistoryRequest(AttrsRawValueAware):
    """
    The request body for notification history.

    https://developer.apple.com/documentation/appstoreserverapi/notificationhistoryrequest
    """

    startDate: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The start date of the timespan for the requested App Store Server Notification history records.

    https://developer.apple.com/documentation/appstoreserverapi/startdate
    """

    endDate: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The end date of the timespan for the requested App Store Server Notification history records.

    https://developer.apple.com/documentation/appstoreserverapi/enddate
    """

    notificationType: Optional[NotificationTypeV2] = NotificationTypeV2.create_main_attr('rawNotificationType', kw_only=True)
    """
    A notification type.

    https://developer.apple.com/documentation/appstoreserverapi/notificationtype
    """

    rawNotificationType: Optional[str] = NotificationTypeV2.create_raw_attr('notificationType')
    """
    See notificationType
    """

    notificationSubtype: Optional[Subtype] = Subtype.create_main_attr('rawNotificationSubtype', kw_only=True)
    """
    A notification subtype.

    https://developer.apple.com/documentation/appstoreserverapi/notificationsubtype
    """

    rawNotificationSubtype: Optional[str] = Subtype.create_raw_attr('notificationSubtype')
    """
    See notificationSubtype
    """

    onlyFailures: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value you set to true to request only the notifications that haven’t reached your server successfully.

    https://developer.apple.com/documentation/appstoreserverapi/onlyfailures
    """

    transactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The transaction identifier, which may be an original transaction identifier, of any transaction belonging to the customer.

    https://developer.apple.com/documentation/appstoreserverapi/transactionid
    """
