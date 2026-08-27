# Copyright (c) 2024 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware
from .TokenType import TokenType

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

    tokenType: Optional[TokenType] = TokenType.create_main_attr('rawTokenType')
    """
    The type of an external purchase custom link token.
    
    https://developer.apple.com/documentation/appstoreservernotifications/tokentype
    """

    rawTokenType: Optional[str] = TokenType.create_raw_attr('tokenType')
    """
    See tokenType
    """

    tokenExpirationDate: Optional[int] = attr.ib(default=None)
    """
    The field of a custom link token that contains the UNIX date, in milliseconds, when the token expires.
    
    https://developer.apple.com/documentation/appstoreservernotifications/tokenexpirationdate
    """