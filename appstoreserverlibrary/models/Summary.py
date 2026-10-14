# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List
from uuid import UUID

from attr import define
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware

@define
class Summary(AttrsRawValueAware):
    """
    The payload data for a subscription-renewal-date extension notification.

    https://developer.apple.com/documentation/appstoreservernotifications/summary
    """

    requestIdentifier: Optional[UUID] = attr.ib(default=None, kw_only=True)
    """
    The UUID that represents a specific request to extend a subscription renewal date.

    https://developer.apple.com/documentation/appstoreservernotifications/requestidentifier
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment', kw_only=True)
    """
    The server environment that the notification applies to, either sandbox or production.

    https://developer.apple.com/documentation/appstoreservernotifications/environment
    """

    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    appAppleId: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the app that the notification applies to.

    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The bundle identifier of the app.

    https://developer.apple.com/documentation/appstoreservernotifications/bundleid
    """

    productId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The product identifier of the auto-renewable subscription that the subscription-renewal-date extension applies to.

    https://developer.apple.com/documentation/appstoreservernotifications/productid
    """

    storefrontCountryCodes: Optional[List[str]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.deep_iterable(attr.validators.max_len(3))))
    """
    A list of country codes that limits the App Store’s attempt to apply the subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreservernotifications/storefrontcountrycodes
    """

    failedCount: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The final count of subscriptions that fail to receive a subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreservernotifications/failedcount
    """

    succeededCount: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The final count of subscriptions that successfully receive a subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreservernotifications/succeededcount
    """
