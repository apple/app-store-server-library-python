# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import List, Optional

from attr import define
import attr

from .BulletPoint import BulletPoint
from .HeaderPosition import HeaderPosition
from .LibraryUtility import AttrsRawValueAware
from .UploadMessageImage import UploadMessageImage

@define
class UploadMessageRequestBody(AttrsRawValueAware):
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

    headerPosition: Optional[HeaderPosition] = HeaderPosition.create_main_attr('rawHeaderPosition')
    """
    The position of header text, which defaults to placing header text above the body.

    https://developer.apple.com/documentation/retentionmessaging/headerposition
    """

    rawHeaderPosition: Optional[str] = HeaderPosition.create_raw_attr('headerPosition')
    """
    See headerPosition
    """

    bulletPoints: Optional[List[BulletPoint]] = attr.ib(default=None, validator=attr.validators.optional(attr.validators.max_len(5)))
    """
    An optional array of bullet points.

    https://developer.apple.com/documentation/retentionmessaging/bulletpoint
    """
