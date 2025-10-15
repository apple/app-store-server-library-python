# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr
from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware

@define
class DecodedRealtimeRequestBody(AttrsRawValueAware):
    """
    The decoded request body the App Store sends to your server to request a real-time retention message.

    https://developer.apple.com/documentation/retentionmessaging/decodedrealtimerequestbody
    """

    originalTransactionId: Optional[str] = attr.ib(default=None)
    """
    The original transaction identifier of the customer's subscription.

    https://developer.apple.com/documentation/retentionmessaging/originaltransactionid
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of the app in the App Store.

    https://developer.apple.com/documentation/retentionmessaging/appappleid
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of the auto-renewable subscription.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """

    userLocale: Optional[str] = attr.ib(default=None)
    """
    The device's locale.

    https://developer.apple.com/documentation/retentionmessaging/locale
    """

    requestIdentifier: Optional[str] = attr.ib(default=None)
    """
    A UUID the App Store server creates to uniquely identify each request.

    https://developer.apple.com/documentation/retentionmessaging/requestidentifier
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment')
    """
    The server environment, either sandbox or production.

    https://developer.apple.com/documentation/retentionmessaging/environment
    """

    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    signedDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature (JWS) data.

    https://developer.apple.com/documentation/retentionmessaging/signeddate
    """