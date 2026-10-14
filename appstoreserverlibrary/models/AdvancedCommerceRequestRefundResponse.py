# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceRequestRefundResponse(AbstractAdvancedCommerceResponse):
    """
    The response body for a transaction refund request.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefundresponse
    """

    signedRenewalInfo: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    Subscription renewal information signed by the App Store, in JSON Web Signature (JWS) format.

    https://developer.apple.com/documentation/advancedcommerceapi/jwsrenewalinfo
    """

    signedTransactionInfo: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    Transaction information signed by the App Store, in JWS Compact Serialization format.

    https://developer.apple.com/documentation/advancedcommerceapi/jwstransaction
    """

    def __init__(self, *, signedTransactionInfo: str, signedRenewalInfo: Optional[str] = None):
        super().__init__(signedRenewalInfo=signedRenewalInfo, signedTransactionInfo=signedTransactionInfo)
