# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .PromotionalOfferSignatureV1 import PromotionalOfferSignatureV1

@define
class PromotionalOffer:
    """
    A promotional offer and message you provide in a real-time response to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffer
    """

    messageIdentifier: Optional[UUID] = attr.ib(default=None)
    """
    The identifier of the message to display to the customer, along with the promotional offer.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    promotionalOfferSignatureV2: Optional[str] = attr.ib(default=None)
    """
    The promotional offer signature in V2 format.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev2
    """

    promotionalOfferSignatureV1: Optional[PromotionalOfferSignatureV1] = attr.ib(default=None)
    """
    The promotional offer signature in V1 format.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffersignaturev1
    """
