# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr

from .NotificationTypeV2 import NotificationTypeV2
from .Subtype import Subtype

@define
class NotificationHistoryRequest: 
    """
    The request body for notification history.
    
    https://developer.apple.com/documentation/appstoreserverapi/notificationhistoryrequest
    """

    startDate: Optional[int] = attr.ib(default=None)
    """
    The start date of the timespan for the requested App Store Server Notification history records. The startDate needs to precede the endDate. Choose a startDate that's within the past 180 days from the current date.
    
    https://developer.apple.com/documentation/appstoreserverapi/startdate
    """

    endDate: Optional[int] = attr.ib(default=None)
    """
    The end date of the timespan for the requested App Store Server Notification history records. Choose an endDate that's later than the startDate. If you choose an endDate in the future, the endpoint automatically uses the current date as the endDate.
    
    https://developer.apple.com/documentation/appstoreserverapi/enddate
    """

    notificationType: Optional[NotificationTypeV2] = attr.ib(default=None)
    """
    A notification type. Provide this field to limit the notification history records to those with this one notification type. For a list of notifications types, see notificationType.
    Include either the transactionId or the notificationType in your query, but not both.
    
    https://developer.apple.com/documentation/appstoreserverapi/notificationtype
    """

    notificationSubtype: Optional[Subtype] = attr.ib(default=None)
    """
    A notification subtype. Provide this field to limit the notification history records to those with this one notification subtype. For a list of subtypes, see subtype. If you specify a notificationSubtype, you need to also specify its related notificationType.
    
    https://developer.apple.com/documentation/appstoreserverapi/notificationsubtype
    """

    transactionId: Optional[str] = attr.ib(default=None)
    """
    The transaction identifier, which may be an original transaction identifier, of any transaction belonging to the customer. Provide this field to limit the notification history request to this one customer.
    Include either the transactionId or the notificationType in your query, but not both.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionid
    """

    onlyFailures: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value you set to true to request only the notifications that haven’t reached your server successfully. The response also includes notifications that the App Store server is currently retrying to send to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/onlyfailures
    """