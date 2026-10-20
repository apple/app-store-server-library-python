# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .ImageSize import ImageSize
from .ImageState import ImageState
from .LibraryUtility import AttrsRawValueAware

@define
class GetImageListResponseItem(AttrsRawValueAware):
    """
    An image identifier and state information for an image.

    https://developer.apple.com/documentation/retentionmessaging/getimagelistresponseitem
    """

    imageIdentifier: Optional[UUID] = attr.ib(default=None, kw_only=True)
    """
    The identifier of the image.

    https://developer.apple.com/documentation/retentionmessaging/imageidentifier
    """

    imageSize: Optional[ImageSize] = ImageSize.create_main_attr('rawImageSize', kw_only=True)
    """
    The size of the image.

    https://developer.apple.com/documentation/retentionmessaging/imagesize
    """

    rawImageSize: Optional[str] = ImageSize.create_raw_attr('imageSize')
    """
    See imageSize
    """

    imageState: Optional[ImageState] = ImageState.create_main_attr('rawImageState', kw_only=True)
    """
    The current state of the image.

    https://developer.apple.com/documentation/retentionmessaging/imagestate
    """

    rawImageState: Optional[str] = ImageState.create_raw_attr('imageState')
    """
    See imageState
    """
