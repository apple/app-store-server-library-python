# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr
from .RetentionMessageState import RetentionMessageState
from .LibraryUtility import AttrsRawValueAware

@define
class GetMessageListResponseItem(AttrsRawValueAware):
    """
    A message identifier and status information for a message.

    https://developer.apple.com/documentation/retentionmessaging/getmessagelistresponseitem
    """

    messageIdentifier: Optional[str] = attr.ib(default=None)
    """
    The identifier of the message.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    messageState: Optional[RetentionMessageState] = RetentionMessageState.create_main_attr('rawMessageState')
    """
    The current state of the message.

    https://developer.apple.com/documentation/retentionmessaging/messagestate
    """

    rawMessageState: Optional[str] = RetentionMessageState.create_raw_attr('messageState')
    """
    See messageState
    """