# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr

@define
class AlternateProduct:
    """
    A switch-plan message and product ID you provide in a real-time response to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/alternateproduct
    """

    messageIdentifier: Optional[str] = attr.ib(default=None)
    """
    The message identifier of the text to display in the switch-plan retention message.

    The message identifier needs to refer to a message that doesn't include an image and that
    has a messageState of APPROVED; otherwise, the retention message fails.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The product identifier of the subscription the retention message suggests for your customer to switch to.

    Use the product identifier in DecodedRealtimeRequestBody to determine the customer's current subscription.
    Choose an alternative subscription from the same subscription group.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """