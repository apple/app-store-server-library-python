# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
from typing import Optional
from uuid import UUID

from attr import define
import attr

@define
class Message:
    """
    A message identifier you provide in a real-time response to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/message
    """

    messageIdentifier: Optional[UUID] = attr.ib(default=None)
    """
    The identifier of the message to display to the customer.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """
