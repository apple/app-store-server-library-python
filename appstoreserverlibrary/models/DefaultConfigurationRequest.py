# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class DefaultConfigurationRequest:
    """
    The request body that contains the default configuration information.

    https://developer.apple.com/documentation/retentionmessaging/defaultconfigurationrequest
    """

    messageIdentifier: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The message identifier of the message to configure as a default message.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """
