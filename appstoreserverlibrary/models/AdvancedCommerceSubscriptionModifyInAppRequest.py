# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List
import attr
from attr import define
from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .HelperValidationUtils import HelperValidationUtils
from .AdvancedCommerceSubscriptionModifyAddItem import AdvancedCommerceSubscriptionModifyAddItem
from .AdvancedCommerceSubscriptionModifyChangeItem import AdvancedCommerceSubscriptionModifyChangeItem
from .AdvancedCommerceSubscriptionModifyDescriptors import AdvancedCommerceSubscriptionModifyDescriptors
from .AdvancedCommerceSubscriptionModifyPeriodChange import AdvancedCommerceSubscriptionModifyPeriodChange
from .AdvancedCommerceSubscriptionModifyRemoveItem import AdvancedCommerceSubscriptionModifyRemoveItem


@define
class AdvancedCommerceSubscriptionModifyInAppRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request data your app provides to make changes to an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyinapprequest
    """

    operation: str = attr.ib(default="MODIFY_SUBSCRIPTION", init=False, on_setattr=attr.setters.frozen)

    version: str = attr.ib(default="1", init=False, on_setattr=attr.setters.frozen)

    transactionId: str = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/transactionid
    """

    retainBillingCycle: bool = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/retainbillingcycle
    """

    addItems: Optional[List[AdvancedCommerceSubscriptionModifyAddItem]] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyadditem
    """

    changeItems: Optional[List[AdvancedCommerceSubscriptionModifyChangeItem]] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifychangeitem
    """

    currency: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    descriptors: Optional[AdvancedCommerceSubscriptionModifyDescriptors] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifydescriptors
    """

    periodChange: Optional[AdvancedCommerceSubscriptionModifyPeriodChange] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyperiodchange
    """

    removeItems: Optional[List[AdvancedCommerceSubscriptionModifyRemoveItem]] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyremoveitem
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """

    taxCode: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """