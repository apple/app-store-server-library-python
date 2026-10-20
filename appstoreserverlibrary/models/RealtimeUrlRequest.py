# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class RealtimeUrlRequest:
    """
    The request body for configuring the URL of your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurlrequest
    """

    realtimeURL: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(256)])
    """
    A string that contains the URL of your Get Retention Message endpoint for configuration.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurl
    """
