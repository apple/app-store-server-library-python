# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional, Dict

from attr import define
import attr

@define
class RealtimeRequestBody:
    """
    The request body the App Store server sends to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/realtimerequestbody
    """

    signedPayload: Optional[str] = attr.ib(default=None)
    """
    The payload in JSON Web Signature (JWS) format, signed by the App Store.

    https://developer.apple.com/documentation/retentionmessaging/signedpayload
    """