# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

@define
class SendTestNotificationResponse: 
    """
    A response that contains the test notification token.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendtestnotificationresponse
    """

    testNotificationToken: Optional[str] = attr.ib(default=None)
    """
    A unique identifier for a notification test that the App Store server sends to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/testnotificationtoken
    """
