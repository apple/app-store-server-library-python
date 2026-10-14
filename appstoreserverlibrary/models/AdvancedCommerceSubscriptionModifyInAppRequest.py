# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceSubscriptionModifyAddItem import AdvancedCommerceSubscriptionModifyAddItem
from .AdvancedCommerceSubscriptionModifyChangeItem import AdvancedCommerceSubscriptionModifyChangeItem
from .AdvancedCommerceSubscriptionModifyDescriptors import AdvancedCommerceSubscriptionModifyDescriptors
from .AdvancedCommerceSubscriptionModifyPeriodChange import AdvancedCommerceSubscriptionModifyPeriodChange
from .AdvancedCommerceSubscriptionModifyRemoveItem import AdvancedCommerceSubscriptionModifyRemoveItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionModifyInAppRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request data your app provides to make changes to an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyinapprequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    operation: str = attr.ib(init=False, default="MODIFY_SUBSCRIPTION", on_setattr=attr.setters.frozen)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyinapprequest
    """

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)
    """
    A number that represents the version of the data structure or Advanced Commerce API.

    https://developer.apple.com/documentation/advancedcommerceapi/version
    """

    retainBillingCycle: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value that determines whether to keep the existing billing cycle with the change you request.

    https://developer.apple.com/documentation/advancedcommerceapi/retainbillingcycle
    """

    transactionId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A unique identifier that the App Store generates for a transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/transactionid
    """

    addItems: Optional[List[AdvancedCommerceSubscriptionModifyAddItem]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    The data your app provides to add items when it makes changes to an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyadditem
    """

    changeItems: Optional[List[AdvancedCommerceSubscriptionModifyChangeItem]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    The data your app provides to change an item of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifychangeitem
    """

    currency: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The three-letter ISO 4217 currency code for the price of a product.

    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    descriptors: Optional[AdvancedCommerceSubscriptionModifyDescriptors] = attr.ib(default=None, kw_only=True)
    """
    The data your app provides to change the description and display name of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifydescriptors
    """

    periodChange: Optional[AdvancedCommerceSubscriptionModifyPeriodChange] = attr.ib(default=None, kw_only=True)
    """
    The data your app provides to change the period of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyperiodchange
    """

    removeItems: Optional[List[AdvancedCommerceSubscriptionModifyRemoveItem]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    The data your app provides to remove an item from an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyremoveitem
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """

    taxCode: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A tax code that applies to a SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """
