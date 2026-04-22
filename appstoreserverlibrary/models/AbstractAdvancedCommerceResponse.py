# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from abc import ABC
from typing import Optional

from attr import define
import attr

@define
class AbstractAdvancedCommerceResponse(ABC):
    signedRenewalInfo: Optional[str] = attr.ib(default=None)
    """
    Subscription renewal information, signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo
    """
    
    signedTransactionInfo: Optional[str] = attr.ib(default=None)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) Compact Serialization format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """