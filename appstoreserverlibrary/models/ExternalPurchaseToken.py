# Copyright (c) 2024 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware

@define
class ExternalPurchaseToken(AttrsRawValueAware):
    """
    The payload data that contains an external purchase token.
    
    https://developer.apple.com/documentation/appstoreservernotifications/externalpurchasetoken
    """

    externalPurchaseId: Optional[str] = attr.ib(default=None)
    """
    The field of an external purchase token that uniquely identifies the token.
    
    https://developer.apple.com/documentation/appstoreservernotifications/externalpurchaseid
    """

    tokenCreationDate: Optional[int] = attr.ib(default=None)
    """
    The field of an external purchase token that contains the UNIX date, in milliseconds, when the system created the token.
    
    https://developer.apple.com/documentation/appstoreservernotifications/tokencreationdate
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreservernotifications/bundleid
    """