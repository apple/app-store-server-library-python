# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .BulletPoint import BulletPoint
from .HeaderPosition import HeaderPosition
from .LibraryUtility import AttrsRawValueAware, validate_not_none
from .UploadMessageImage import UploadMessageImage

@define
class UploadMessageRequestBody(AttrsRawValueAware):
    """
    The request body for uploading a message, which includes the message text and an optional image reference and bullet points.

    https://developer.apple.com/documentation/retentionmessaging/uploadmessagerequestbody
    """

    header: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(66)])
    """
    The header text of the retention message that the system displays to customers.

    https://developer.apple.com/documentation/retentionmessaging/header
    """

    body: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(144)])
    """
    The body text of the retention message that the system displays to customers.

    https://developer.apple.com/documentation/retentionmessaging/body
    """

    image: Optional[UploadMessageImage] = attr.ib(default=None, kw_only=True)
    """
    The optional image identifier and its alternative text to appear as part of a text-based message with an image.

    https://developer.apple.com/documentation/retentionmessaging/uploadmessageimage
    """

    bulletPoints: Optional[List[BulletPoint]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.max_len(5)))
    """
    An optional array of up to five bullet points.

    https://developer.apple.com/documentation/retentionmessaging/bulletpoint
    """

    headerPosition: Optional[HeaderPosition] = HeaderPosition.create_main_attr('rawHeaderPosition', kw_only=True)
    """
    The position of header text, which defaults to placing header text above the body.

    https://developer.apple.com/documentation/retentionmessaging/headerposition
    """

    rawHeaderPosition: Optional[str] = HeaderPosition.create_raw_attr('headerPosition')
    """
    See headerPosition
    """
