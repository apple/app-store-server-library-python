# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

@define
class MassExtendRenewalDateStatusResponse: 
    """
    A response that indicates the current status of a request to extend the subscription renewal date to all eligible subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldatestatusresponse
    """

    requestIdentifier: Optional[str] = attr.ib(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    complete: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether the App Store completed the request to extend a subscription renewal date to active subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/complete
    """

    completeDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the App Store completes a request to extend a subscription renewal date for eligible subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/completedate
    """

    succeededCount: Optional[int] = attr.ib(default=None)
    """
    The count of subscriptions that successfully receive a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/succeededcount
    """

    failedCount: Optional[int] = attr.ib(default=None)
    """
    The count of subscriptions that fail to receive a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/failedcount
    """