# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr
from .PromotionalOfferSignatureV1 import PromotionalOfferSignatureV1

@define
class PromotionalOffer:
    """
    A promotional offer and message you provide in a real-time response to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffer
    """

    messageIdentifier: Optional[str] = attr.ib(default=None)
    """
    The identifier of the message to display to the customer, along with the promotional offer.

    The message identifier needs to refer to a message that doesn't have an image, and that has
    a messageState of APPROVED; otherwise, the retention message fails.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    promotionalOfferSignatureV2: Optional[str] = attr.ib(default=None)
    """
    The promotional offer signature in V2 format. This field is mutually exclusive with
    promotionalOfferSignatureV1 field.

    For new implementations, consider using this V2 signature, which is easier to generate.
    To generate this signature, use the PromotionalOfferV2SignatureCreator class:

    Example:
        from appstoreserverlibrary.jws_signature_creator import PromotionalOfferV2SignatureCreator

        creator = PromotionalOfferV2SignatureCreator(signing_key, key_id, issuer_id, bundle_id)
        signature = creator.create_signature(
            product_id="com.example.subscription",
            offer_identifier="intro_offer",
            transaction_id="optional_transaction_id"
        )

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev2
    """

    promotionalOfferSignatureV1: Optional[PromotionalOfferSignatureV1] = attr.ib(default=None)
    """
    The promotional offer signature in V1 format. This field is mutually exclusive with the
    promotionalOfferSignatureV2 field.

    To generate this signature, use the PromotionalOfferSignatureCreator class.
    See PromotionalOfferSignatureV1 for implementation details.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """