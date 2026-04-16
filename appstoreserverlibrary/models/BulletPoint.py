# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

@define
class BulletPoint:
    """
    The text and its bullet-point image to include in a retention message’s bulleted list.

    https://developer.apple.com/documentation/retentionmessaging/bulletpoint
    """

    text: str = attr.ib(validator=attr.validators.max_len(66))
    """
    The text of the individual bullet point.

    https://developer.apple.com/documentation/retentionmessaging/bulletpointtext
    """

    imageIdentifier: UUID = attr.ib()
    """
    The identifier of the image to use as the bullet point.

    https://developer.apple.com/documentation/retentionmessaging/imageidentifier
    """

    altText: str = attr.ib(validator=attr.validators.max_len(150))
    """
    The alternative text you provide for the corresponding image of the bullet point.

    https://developer.apple.com/documentation/retentionmessaging/alttext
    """
