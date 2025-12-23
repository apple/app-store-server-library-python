# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware

@define
class AppData(AttrsRawValueAware):
    """
    The object that contains the app metadata and signed app transaction information.

    https://developer.apple.com/documentation/appstoreservernotifications/appdata
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of the app that the notification applies to.

    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of the app.

    https://developer.apple.com/documentation/appstoreservernotifications/bundleid
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

    signedAppTransactionInfo: Optional[str] = attr.ib(default=None)
    """
    App transaction information signed by the App Store, in JSON Web Signature (JWS) format.

    https://developer.apple.com/documentation/appstoreservernotifications/jwsapptransaction
    """
