# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class DefaultConfigurationResponse:
    """
    The response body that contains the default configuration information.

    https://developer.apple.com/documentation/retentionmessaging/defaultconfigurationresponse
    """

    messageIdentifier: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The message identifier of the retention message you configured as a default.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """
