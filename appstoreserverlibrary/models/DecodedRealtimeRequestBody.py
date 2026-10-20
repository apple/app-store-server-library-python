# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware, validate_not_none

@define
class DecodedRealtimeRequestBody(AttrsRawValueAware):
    """
    The decoded request body the App Store sends to your server to request a real-time retention message.

    https://developer.apple.com/documentation/retentionmessaging/decodedrealtimerequestbody
    """

    originalTransactionId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The original transaction identifier of the customer’s subscription.

    https://developer.apple.com/documentation/retentionmessaging/originaltransactionid
    """

    appAppleId: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The unique identifier of the app in the App Store.

    https://developer.apple.com/documentation/retentionmessaging/appappleid
    """

    productId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The unique identifier of the auto-renewable subscription.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """

    userLocale: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The device’s locale.

    https://developer.apple.com/documentation/retentionmessaging/locale
    """

    requestIdentifier: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A UUID the App Store server creates to uniquely identify each request.

    https://developer.apple.com/documentation/retentionmessaging/requestidentifier
    """

    environment: Environment = Environment.create_main_attr('rawEnvironment', raw_required=True, kw_only=True)
    """
    The server environment, either sandbox or production.

    https://developer.apple.com/documentation/retentionmessaging/environment
    """

    rawEnvironment: str = Environment.create_raw_attr('environment', required=True)
    """
    See environment
    """

    signedDate: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature (JWS) data.

    https://developer.apple.com/documentation/retentionmessaging/signeddate
    """
