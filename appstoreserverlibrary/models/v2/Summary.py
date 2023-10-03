# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
from typing import List, Optional
import attr
from pydantic import Field

from .Base import Model
from .Environment import Environment


class Summary(Model):
    """
    The payload data for a subscription-renewal-date extension notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/summary
    """

    environment: Optional[Environment] = Field(default=None)
    """
    The server environment that the notification applies to, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreservernotifications/environment
    """

    appAppleId: Optional[int] = Field(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = Field(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    productId: Optional[str] = Field(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    requestIdentifier: Optional[str] = Field(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    storefrontCountryCodes: Optional[List[str]] = Field(default=None)
    """
    A list of storefront country codes you provide to limit the storefronts for a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefrontcountrycodes
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
