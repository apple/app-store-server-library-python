# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest

@define
class AdvancedCommerceSubscriptionCancelRequest(AdvancedCommerceRequest):
    """
    The request body for turning off automatic renewal of a subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncancelrequest
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """