# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
from appstoreserverlibrary.models.AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse


@define
class AdvancedCommerceSubscriptionRevokeResponse(AbstractAdvancedCommerceResponse):
    """
    The response body for a successful revoke-subscription request.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionrevokeresponse
    """
    def __init__(self, signedRenewalInfo: str, signedTransactionInfo: str):
        super().__init__(signedRenewalInfo=signedRenewalInfo, signedTransactionInfo=signedTransactionInfo)