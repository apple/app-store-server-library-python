# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware
from .SendAttemptResult import SendAttemptResult

@define
class SendAttemptItem(AttrsRawValueAware):
    """
    The success or error information and the date the App Store server records when it attempts to send a server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptitem
    """

    attemptDate: Optional[int] = attr.ib(default=None)
    """
    The date the App Store server attempts to send a notification.
    
    https://developer.apple.com/documentation/appstoreserverapi/attemptdate
    """

    sendAttemptResult: Optional[SendAttemptResult] = SendAttemptResult.create_main_attr('rawSendAttemptResult')
    """
    The success or error information the App Store server records when it attempts to send an App Store server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptresult
    """
        
    rawSendAttemptResult: Optional[str] = SendAttemptResult.create_raw_attr('sendAttemptResult')
    """
    See sendAttemptResult
    """