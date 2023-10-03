# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from .Base import Model
from .SendAttemptResult import SendAttemptResult


class SendAttemptItem(Model):
    """
    The success or error information and the date the App Store server records when it attempts to send a server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptitem
    """

    attemptDate: Optional[int] = Field(default=None)
    """
    The date the App Store server attempts to send a notification.
    
    https://developer.apple.com/documentation/appstoreserverapi/attemptdate
    """

    sendAttemptResult: Optional[SendAttemptResult] = Field(default=None)
    """
    The success or error information the App Store server records when it attempts to send an App Store server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptresult
    """
