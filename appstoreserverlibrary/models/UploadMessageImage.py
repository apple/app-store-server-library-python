# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr

@define
class UploadMessageImage:
    """
    The definition of an image with its alternative text.

    https://developer.apple.com/documentation/retentionmessaging/uploadmessageimage
    """

    imageIdentifier: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of an image.

    https://developer.apple.com/documentation/retentionmessaging/imageidentifier
    """

    altText: Optional[str] = attr.ib(default=None)
    """
    The alternative text you provide for the corresponding image.
    Maximum length: 150

    https://developer.apple.com/documentation/retentionmessaging/alttext
    """