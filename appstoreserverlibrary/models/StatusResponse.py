# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr
from .Environment import Environment
from .SubscriptionGroupIdentifierItem import SubscriptionGroupIdentifierItem

@define
class StatusResponse: 
    """
    A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
    
    https://developer.apple.com/documentation/appstoreserverapi/statusresponse
    """

    environment: Environment = attr.ib(default=None)
    """
    The server environment, sandbox or production, in which the App Store generated the response.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    bundleId: str = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    appAppleId: int = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    data: "list[SubscriptionGroupIdentifierItem]" = attr.ib(default=None)
    """
    An array of information for auto-renewable subscriptions, including App Store-signed transaction information and App Store-signed renewal information.
    
    """