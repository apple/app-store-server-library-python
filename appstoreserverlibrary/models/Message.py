# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr

@define
class Message:
    """
    A message identifier you provide in a real-time response to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/message
    """

    messageIdentifier: Optional[str] = attr.ib(default=None)
    """
    The identifier of the message to display to the customer.

    The message identifier needs to refer to a message that has a messageState of APPROVED;
    otherwise, the retention message fails. If the message includes an image, the image also
    needs to have an imageState of APPROVED.

    For more information about setting up messages, see Upload Message.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """