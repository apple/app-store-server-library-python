# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from appstoreserverlibrary.models.v2.Base import Model


class SendTestNotificationResponse(Model):
    """
    A response that contains the test notification token.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendtestnotificationresponse
    """

    testNotificationToken: Optional[str] = Field(default=None)
    """
    A unique identifier for a notification test that the App Store server sends to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/testnotificationtoken
    """
