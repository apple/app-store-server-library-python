# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

@define
class ResponseBodyV2:
    """
    The response body the App Store sends in a version 2 server notification.

    https://developer.apple.com/documentation/appstoreservernotifications/responsebodyv2
    """
     
    signedPayload: Optional[str] = attr.ib(default=None)
    """
    A cryptographically signed payload, in JSON Web Signature (JWS) format, containing the response body for a version 2 notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/signedpayload
    """
