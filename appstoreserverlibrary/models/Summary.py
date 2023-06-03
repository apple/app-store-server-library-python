# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
from typing import List
import attr
from .Environment import Environment

@define
class Summary: 
    """
    The payload data for a subscription-renewal-date extension notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/summary
    """

    environment: Environment = attr.ib(default=None)
    """
    The server environment that the notification applies to, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreservernotifications/environment
    """

    appAppleId: int = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: str = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    productId: str = attr.ib(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """    

    requestIdentifier: str = attr.ib(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    storefrontCountryCodes: "List[str]" = attr.ib(default=None)
    """
    A list of storefront country codes you provide to limit the storefronts for a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefrontcountrycodes
    """

    succeededCount: int = attr.ib(default=None)
    """
    The count of subscriptions that successfully receive a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/succeededcount
    """

    failedCount: int = attr.ib(default=None)
    """
    The count of subscriptions that fail to receive a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/failedcount
    """