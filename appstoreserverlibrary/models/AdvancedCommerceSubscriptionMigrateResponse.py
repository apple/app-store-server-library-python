# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse


@define
class AdvancedCommerceSubscriptionMigrateResponse(AbstractAdvancedCommerceResponse):
    """
    A response that contains signed renewal and transaction information after a subscription successfully migrates to the Advanced Commerce API.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigrateresponse
    """
    def __init__(self, signedRenewalInfo: str, signedTransactionInfo: str):
        super().__init__(signedRenewalInfo=signedRenewalInfo, signedTransactionInfo=signedTransactionInfo)