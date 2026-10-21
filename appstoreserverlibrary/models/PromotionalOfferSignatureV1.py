# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class PromotionalOfferSignatureV1:
    """
    The promotional-offer signature you generate using an earlier signature version.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    encodedSignature: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The Base64-encoded cryptographic signature you generate using the offer parameters.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    productId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The subscription’s product identifier.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """

    nonce: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A one-time-use UUID antireplay value you generate.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    timestamp: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The UNIX time, in milliseconds, when you generate the signature.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    keyId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A string that identifies the private key you use to generate the signature.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    offerIdentifier: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The subscription offer identifier that you set up in App Store Connect.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    appAccountToken: Optional[UUID] = attr.ib(default=None, kw_only=True)
    """
    A UUID that you provide to associate with the transaction if the customer accepts the promotional offer.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """
