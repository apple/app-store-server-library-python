# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class RealtimeUrlResponse:
    """
    The response body that contains the URL for your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurlresponse
    """

    realtimeURL: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(256)])
    """
    A string that contains the URL you provided for your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurl
    """
