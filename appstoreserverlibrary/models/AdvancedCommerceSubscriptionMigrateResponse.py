# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionMigrateResponse(AbstractAdvancedCommerceResponse):
    """
    A response that contains signed renewal and transaction information after a subscription successfully migrates to the Advanced Commerce API.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigrateresponse
    """

    signedRenewalInfo: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    Subscription renewal information signed by the App Store, in JSON Web Signature (JWS) format, for the migrated subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/jwsrenewalinfo
    """

    signedTransactionInfo: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) Compact Serialization format, for the migrated subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/jwstransaction
    """

    def __init__(self, *, signedRenewalInfo: str, signedTransactionInfo: str):
        super().__init__(signedRenewalInfo=signedRenewalInfo, signedTransactionInfo=signedTransactionInfo)
