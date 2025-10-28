# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

@define
class PromotionalOfferSignatureV1:
    """
    The promotional offer signature you generate using an earlier signature version.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    encodedSignature: str = attr.ib()
    """
    The Base64-encoded cryptographic signature you generate using the offer parameters.
    """

    productId: str = attr.ib()
    """
    The subscription's product identifier.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """

    nonce: UUID = attr.ib()
    """
    A one-time-use UUID antireplay value you generate.
    """

    timestamp: int = attr.ib()
    """
    The UNIX time, in milliseconds, when you generate the signature.
    """

    keyId: str = attr.ib()
    """
    A string that identifies the private key you use to generate the signature.
    """

    offerIdentifier: str = attr.ib()
    """
    The subscription offer identifier that you set up in App Store Connect.
    """

    appAccountToken: Optional[UUID] = attr.ib(default=None)
    """
    A UUID that you provide to associate with the transaction if the customer accepts the promotional offer.
    """
