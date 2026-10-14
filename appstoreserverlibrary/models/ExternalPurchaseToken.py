# Copyright (c) 2024 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware, validate_not_none
from .TokenType import TokenType

@define
class ExternalPurchaseToken(AttrsRawValueAware):
    """
    The payload data that contains an external purchase token.

    https://developer.apple.com/documentation/appstoreservernotifications/externalpurchasetoken
    """

    externalPurchaseId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The unique identifier of the token.

    https://developer.apple.com/documentation/appstoreservernotifications/externalpurchaseid
    """

    tokenCreationDate: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The UNIX time, in milliseconds, when the system created the token.

    https://developer.apple.com/documentation/appstoreservernotifications/tokencreationdate
    """

    appAppleId: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The app Apple ID for which the system generated the token.

    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The bundle ID of the app for which the system generated the token.

    https://developer.apple.com/documentation/appstoreservernotifications/bundleid
    """

    tokenExpirationDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, when a token expires.

    https://developer.apple.com/documentation/appstoreservernotifications/tokenexpirationdate
    """

    tokenType: Optional[TokenType] = TokenType.create_main_attr('rawTokenType', kw_only=True)
    """
    The custom link token type, either SERVICES or ACQUISITION.

    https://developer.apple.com/documentation/appstoreservernotifications/tokentype
    """

    rawTokenType: Optional[str] = TokenType.create_raw_attr('tokenType')
    """
    See tokenType
    """
