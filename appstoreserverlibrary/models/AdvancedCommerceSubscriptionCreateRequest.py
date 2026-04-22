# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List
import attr
from attr import define
from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from .AdvancedCommerceSubscriptionCreateItem import AdvancedCommerceSubscriptionCreateItem
from .AdvancedCommercePeriod import AdvancedCommercePeriod


@define
class AdvancedCommerceSubscriptionCreateRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request data your app provides when a customer purchases an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreaterequest
    """

    operation: str = attr.ib(init=False, default="CREATE_SUBSCRIPTION", on_setattr=attr.setters.frozen)

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)

    currency: str = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    descriptors: AdvancedCommerceDescriptors = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/descriptors
    """

    items: List[AdvancedCommerceSubscriptionCreateItem] = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreateitem
    """

    taxCode: str = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/taxCode
    """

    period: AdvancedCommercePeriod = AdvancedCommercePeriod.create_main_attr('rawPeriod', raw_required=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/period
    """

    rawPeriod: str = AdvancedCommercePeriod.create_raw_attr('period', required=True)
    """
    See period
    """

    previousTransactionId: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/transactionid
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """