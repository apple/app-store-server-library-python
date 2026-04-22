# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse

class AdvancedCommerceSubscriptionChangeMetadataResponse(AbstractAdvancedCommerceResponse):
    """
    The response body for a successful subscription metadata change.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadataresponse
    """

    def __init__(self, signedRenewalInfo: str, signedTransactionInfo: str):
        super().__init__(signedRenewalInfo=signedRenewalInfo, signedTransactionInfo=signedTransactionInfo)