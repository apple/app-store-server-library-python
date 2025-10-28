# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .UploadMessageImage import UploadMessageImage

@define
class UploadMessageRequestBody:
    """
    The request body for uploading a message, which includes the message text and an optional image reference.

    https://developer.apple.com/documentation/retentionmessaging/uploadmessagerequestbody
    """

    header: str = attr.ib(validator=attr.validators.max_len(66))
    """
    The header text of the retention message that the system displays to customers.

    https://developer.apple.com/documentation/retentionmessaging/header
    """

    body: str = attr.ib(validator=attr.validators.max_len(144))
    """
    The body text of the retention message that the system displays to customers.

    https://developer.apple.com/documentation/retentionmessaging/body
    """

    image: Optional[UploadMessageImage] = attr.ib(default=None)
    """
    The optional image identifier and its alternative text to appear as part of a text-based message with an image.

    https://developer.apple.com/documentation/retentionmessaging/uploadmessageimage
    """
