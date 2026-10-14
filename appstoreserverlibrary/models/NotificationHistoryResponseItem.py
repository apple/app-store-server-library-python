# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .SendAttemptItem import SendAttemptItem

@define
class NotificationHistoryResponseItem:
    """
    The App Store server notification history record, including the signed notification payload and the result of the server’s first send attempt.

    https://developer.apple.com/documentation/appstoreserverapi/notificationhistoryresponseitem
    """

    sendAttempts: Optional[List[SendAttemptItem]] = attr.ib(default=None, kw_only=True)
    """
    An array of information the App Store server records for its attempts to send a notification to your server.

    https://developer.apple.com/documentation/appstoreserverapi/sendattemptitem
    """

    signedPayload: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The cryptographically signed payload, in JSON Web Signature (JWS) format, containing the original response body of a version 2 notification.

    https://developer.apple.com/documentation/appstoreserverapi/signedpayload
    """
