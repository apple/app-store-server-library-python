# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr

@define
class PromotionalOfferSignatureV1:
    """
    The promotional offer signature you generate using an earlier signature version.

    To generate this signature, use the PromotionalOfferSignatureCreator class:

    Example:
        from appstoreserverlibrary.promotional_offer import PromotionalOfferSignatureCreator
        import uuid
        import time

        creator = PromotionalOfferSignatureCreator(signing_key, key_id, bundle_id)
        signature = creator.create_signature(
            product_identifier="com.example.subscription",
            subscription_offer_id="intro_offer",
            application_username="user123",
            nonce=uuid.uuid4(),
            timestamp=int(time.time() * 1000)
        )

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """

    encodedSignature: Optional[str] = attr.ib(default=None)
    """
    The Base64-encoded cryptographic signature you generate using the offer parameters.

    https://developer.apple.com/documentation/retentionmessaging/encodedsignature
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The subscription's product identifier.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """

    nonce: Optional[str] = attr.ib(default=None)
    """
    A one-time-use UUID antireplay value you generate. Use lowercase.

    https://developer.apple.com/documentation/retentionmessaging/nonce
    """

    offerId: Optional[str] = attr.ib(default=None)
    """
    The promotional offer's identifier.

    https://developer.apple.com/documentation/retentionmessaging/offerid
    """

    timestamp: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that you generate the signature.

    https://developer.apple.com/documentation/retentionmessaging/timestamp
    """

    keyIdentifier: Optional[str] = attr.ib(default=None)
    """
    Your private key identifier from App Store Connect.

    https://developer.apple.com/documentation/retentionmessaging/keyidentifier
    """