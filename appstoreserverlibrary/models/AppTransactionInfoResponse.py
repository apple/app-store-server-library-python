# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

@define
class AppTransactionInfoResponse:
    """
    A response that contains signed app transaction information for a customer.
    
    https://developer.apple.com/documentation/appstoreserverapi/apptransactioninforesponse
    """
    
    signedAppTransactionInfo: Optional[str] = attr.ib(default=None)
    """
    A customer’s app transaction information, signed by Apple, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsapptransaction
    """