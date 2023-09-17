# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from appstoreserverlibrary.models.v2.Base import Model


class MassExtendRenewalDateStatusResponse(Model):
    """
    A response that indicates the current status of a request to extend the subscription renewal date to all eligible subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldatestatusresponse
    """

    requestIdentifier: Optional[str] = Field(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    complete: Optional[bool] = Field(default=None)
    """
    A Boolean value that indicates whether the App Store completed the request to extend a subscription renewal date to active subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/complete
    """

    completeDate: Optional[int] = Field(default=None)
    """
    The UNIX time, in milliseconds, that the App Store completes a request to extend a subscription renewal date for eligible subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/completedate
    """

    succeededCount: Optional[int] = Field(default=None)
    """
    The count of subscriptions that successfully receive a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/succeededcount
    """

    failedCount: Optional[int] = Field(default=None)
    """
    The count of subscriptions that fail to receive a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/failedcount
    """