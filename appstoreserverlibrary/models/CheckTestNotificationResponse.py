# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import List, Optional

from attr import define
import attr

from .SendAttemptItem import SendAttemptItem

@define
class CheckTestNotificationResponse: 
    """
    A response that contains the contents of the test notification sent by the App Store server and the result from your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/checktestnotificationresponse
    """

    signedPayload: Optional[str] = attr.ib(default=None)
    """
    A cryptographically signed payload, in JSON Web Signature (JWS) format, containing the response body for a version 2 notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/signedpayload
    """

    sendAttempts: Optional[List[SendAttemptItem]] = attr.ib(default=None)
    """
    An array of information the App Store server records for its attempts to send the TEST notification to your server. The array may contain a maximum of six sendAttemptItem objects.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptitem
    """