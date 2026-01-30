# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from __future__ import annotations
from typing import List, Optional
import attr
from appstoreserverlibrary.models.AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionReactivateItem import AdvancedCommerceSubscriptionReactivateItem

@attr.define
class AdvancedCommerceSubscriptionReactivateInAppRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request your app provides to reactivate a subscription that has automatic renewal turned off.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateinapprequest
    """
    operation: str = attr.ib(init=False, default="REACTIVATE_SUBSCRIPTION", on_setattr=attr.setters.frozen)

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)

    transactionId: str = attr.ib()
    """
    https://developer.apple.com/documentation/appstoreserverapi/transactionid
    """
    
    items: Optional[List[AdvancedCommerceSubscriptionReactivateItem]] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateitem
    """
    
    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """