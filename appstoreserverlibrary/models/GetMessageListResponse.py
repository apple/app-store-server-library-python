# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List
from attr import define
import attr
from .GetMessageListResponseItem import GetMessageListResponseItem

@define
class GetMessageListResponse:
    """
    A response that contains status information for all messages.

    https://developer.apple.com/documentation/retentionmessaging/getmessagelistresponse
    """

    messageIdentifiers: Optional[List[GetMessageListResponseItem]] = attr.ib(default=None)
    """
    An array of all message identifiers and their message states.

    https://developer.apple.com/documentation/retentionmessaging/getmessagelistresponseitem
    """