# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse


@define
class AdvancedCommerceSubscriptionPriceChangeResponse(AbstractAdvancedCommerceResponse):
    """
    A response that contains signed JWS renewal and JWS transaction information after a subscription price change request.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangeresponse
    """
    def __init__(self, signedRenewalInfo: str, signedTransactionInfo: str):
        super().__init__(signedRenewalInfo=signedRenewalInfo, signedTransactionInfo=signedTransactionInfo)