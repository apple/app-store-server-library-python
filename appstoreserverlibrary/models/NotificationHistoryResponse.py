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

    notificationHistory: Optional[List[NotificationHistoryResponseItem]] = attr.ib(default=None, kw_only=True)
    """
    An array of App Store Server Notifications history records.

    https://developer.apple.com/documentation/appstoreserverapi/notificationhistoryresponseitem
    """

    hasMore: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the App Store has more notification history records to send.

    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """

    paginationToken: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A pagination token that you provide to Get Notification History on a subsequent request to get the next page of responses.

    https://developer.apple.com/documentation/appstoreserverapi/paginationtoken
    """
