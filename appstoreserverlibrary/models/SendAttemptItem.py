# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .SendAttemptResult import SendAttemptResult

@define
class SendAttemptItem: 
    """
    The success or error information and the date the App Store server records when it attempts to send a server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptitem
    """

    attemptDate: int = attr.ib(default=None)
    """
    The date the App Store server attempts to send a notification.
    
    https://developer.apple.com/documentation/appstoreserverapi/attemptdate
    """

    sendAttemptResult: SendAttemptResult = attr.ib(default=None)
    """
    The success or error information the App Store server records when it attempts to send an App Store server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/sendattemptresult
    """