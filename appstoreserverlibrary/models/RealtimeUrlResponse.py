# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

@define
class RealtimeUrlResponse:
    """
    The response body that contains the URL for your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurlresponse
    """

    realtimeURL: Optional[str] = attr.ib()
    """
    A string that contains the URL you provided for your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/realtimeurl
    """
