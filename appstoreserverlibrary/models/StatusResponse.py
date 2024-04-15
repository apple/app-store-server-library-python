# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional, List

from attr import define
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware
from .SubscriptionGroupIdentifierItem import SubscriptionGroupIdentifierItem

@define
class StatusResponse(AttrsRawValueAware):
    """
    A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
    
    https://developer.apple.com/documentation/appstoreserverapi/statusresponse
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment')
    """
    The server environment, sandbox or production, in which the App Store generated the response.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """
            
    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    data: Optional[List[SubscriptionGroupIdentifierItem]] = attr.ib(default=None)
    """
    An array of information for auto-renewable subscriptions, including App Store-signed transaction information and App Store-signed renewal information.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifieritem
    """