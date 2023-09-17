# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional, List

from pydantic import Field

from .Base import Model
from .Environment import Environment
from .SubscriptionGroupIdentifierItem import SubscriptionGroupIdentifierItem


class StatusResponse(Model):
    """
    A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
    
    https://developer.apple.com/documentation/appstoreserverapi/statusresponse
    """

    environment: Optional[Environment] = Field(default=None)
    """
    The server environment, sandbox or production, in which the App Store generated the response.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    bundleId: Optional[str] = Field(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    appAppleId: Optional[int] = Field(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    data: Optional[List[SubscriptionGroupIdentifierItem]] = Field(default=None)
    """
    An array of information for auto-renewable subscriptions, including App Store-signed transaction information and App Store-signed renewal information.
    
    """
