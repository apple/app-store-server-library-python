# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .Message import Message
from .AlternateProduct import AlternateProduct
from .PromotionalOffer import PromotionalOffer

@define
class RealtimeResponseBody:
    """
    A response you provide to choose, in real time, a retention message the system displays to the customer.

    https://developer.apple.com/documentation/retentionmessaging/realtimeresponsebody
    """

    message: Optional[Message] = attr.ib(default=None)
    """
    A retention message that's text-based and can include an optional image.

    https://developer.apple.com/documentation/retentionmessaging/message
    """

    alternateProduct: Optional[AlternateProduct] = attr.ib(default=None)
    """
    A retention message with a switch-plan option.

    https://developer.apple.com/documentation/retentionmessaging/alternateproduct
    """

    promotionalOffer: Optional[PromotionalOffer] = attr.ib(default=None)
    """
    A retention message that includes a promotional offer.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffer
    """
