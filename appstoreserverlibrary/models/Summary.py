# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
from typing import List, Optional
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware

@define
class Summary(AttrsRawValueAware):
    """
    The payload data for a subscription-renewal-date extension notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/summary
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment')
    """
    The server environment that the notification applies to, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreservernotifications/environment
    """
           
    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """    

    requestIdentifier: Optional[str] = attr.ib(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    storefrontCountryCodes: Optional[List[str]] = attr.ib(default=None)
    """
    A list of storefront country codes you provide to limit the storefronts for a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefrontcountrycodes
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