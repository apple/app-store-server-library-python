# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .GetImageListResponseItem import GetImageListResponseItem

@define
class GetImageListResponse:
    """
    A response that contains status information for all images.

    https://developer.apple.com/documentation/retentionmessaging/getimagelistresponse
    """

    imageIdentifiers: Optional[List[GetImageListResponseItem]] = attr.ib(default=None)
    """
    An array of all image identifiers and their image state.

    https://developer.apple.com/documentation/retentionmessaging/getimagelistresponseitem
    """
