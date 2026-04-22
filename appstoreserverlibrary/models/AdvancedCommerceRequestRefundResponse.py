# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse

class AdvancedCommerceRequestRefundResponse(AbstractAdvancedCommerceResponse):
    """
    The response body for a transaction refund request.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefundresponse
    """

    def __init__(self, signedTransactionInfo: str):
        super().__init__(signedRenewalInfo=None, signedTransactionInfo=signedTransactionInfo)