# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .SendAttemptItem import SendAttemptItem

@define
class CheckTestNotificationResponse:
    """
    A response that contains the contents of the App Store server’s test notification and the result from your server.

    https://developer.apple.com/documentation/appstoreserverapi/checktestnotificationresponse
    """

    sendAttempts: Optional[List[SendAttemptItem]] = attr.ib(default=None, kw_only=True)
    """
    An array of information the App Store server records for its attempts to send the TEST notification to your server.

    https://developer.apple.com/documentation/appstoreserverapi/sendattemptitem
    """

    signedPayload: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The signed payload, in JWS format, that contains the TEST notification that the App Store server sent to your server.

    https://developer.apple.com/documentation/appstoreserverapi/signedpayload
    """
