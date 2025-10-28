# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .MessageState import MessageState
from .LibraryUtility import AttrsRawValueAware

@define
class GetMessageListResponseItem(AttrsRawValueAware):
    """
    A message identifier and status information for a message.

    https://developer.apple.com/documentation/retentionmessaging/getmessagelistresponseitem
    """

    messageIdentifier: Optional[UUID] = attr.ib(default=None)
    """
    The identifier of the message.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    messageState: Optional[MessageState] = MessageState.create_main_attr('rawMessageState')
    """
    The current state of the message.

    https://developer.apple.com/documentation/retentionmessaging/messageState
    """

    rawMessageState: Optional[str] = MessageState.create_raw_attr('messageState')
    """
    See messageState
    """