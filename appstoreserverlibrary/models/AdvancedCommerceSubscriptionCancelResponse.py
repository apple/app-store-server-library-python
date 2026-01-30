# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define

from .AbstractAdvancedCommerceResponse import AbstractAdvancedCommerceResponse

@define
class AdvancedCommerceSubscriptionCancelResponse(AbstractAdvancedCommerceResponse):
    """
    The response body for a successful subscription cancellation.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncancelresponse
    """
    pass