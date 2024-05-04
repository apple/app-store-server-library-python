# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional, List

from attr import define
import attr

from .NotificationHistoryResponseItem import NotificationHistoryResponseItem

@define
class NotificationHistoryResponse: 
    """
    A response that contains the App Store Server Notifications history for your app.
    
    https://developer.apple.com/documentation/appstoreserverapi/notificationhistoryresponse
    """

    paginationToken: Optional[str] = attr.ib(default=None)
    """
    A pagination token that you return to the endpoint on a subsequent call to receive the next set of results.
    
    https://developer.apple.com/documentation/appstoreserverapi/paginationtoken
    """

    hasMore: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value indicating whether the App Store has more transaction data.
    
    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """

    notificationHistory: Optional[List[NotificationHistoryResponseItem]] = attr.ib(default=None)
    """
    An array of App Store server notification history records.
    
    https://developer.apple.com/documentation/appstoreserverapi/notificationhistoryresponseitem
    """
