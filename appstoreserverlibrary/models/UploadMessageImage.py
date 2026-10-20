# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class UploadMessageImage:
    """
    The definition of an image with its alternative text.

    https://developer.apple.com/documentation/retentionmessaging/uploadmessageimage
    """

    imageIdentifier: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The unique identifier of an image.

    https://developer.apple.com/documentation/retentionmessaging/imageidentifier
    """

    altText: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(150)])
    """
    The alternative text you provide for the corresponding image.

    https://developer.apple.com/documentation/retentionmessaging/alttext
    """
