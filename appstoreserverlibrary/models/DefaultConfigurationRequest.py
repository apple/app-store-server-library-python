# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from attr import define
import attr

@define
class DefaultConfigurationRequest:
    """
    The request body that contains the default configuration information.

    https://developer.apple.com/documentation/retentionmessaging/defaultconfigurationrequest
    """

    messageIdentifier: Optional[str] = attr.ib(default=None)
    """
    The message identifier of the message to configure as a default message.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """
