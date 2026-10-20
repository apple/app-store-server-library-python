# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from .AdvancedCommercePeriod import AdvancedCommercePeriod
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceSubscriptionCreateItem import AdvancedCommerceSubscriptionCreateItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionCreateRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request data your app provides when a customer purchases an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreaterequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    operation: str = attr.ib(init=False, default="CREATE_SUBSCRIPTION", on_setattr=attr.setters.frozen)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreaterequest
    """

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)
    """
    A number that represents the version of the data structure or Advanced Commerce API.

    https://developer.apple.com/documentation/advancedcommerceapi/version
    """

    currency: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The three-letter ISO 4217 currency code for the price of a product.

    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    descriptors: AdvancedCommerceDescriptors = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The display name and description of a subscription product.

    https://developer.apple.com/documentation/advancedcommerceapi/descriptors
    """

    items: List[AdvancedCommerceSubscriptionCreateItem] = attr.ib(kw_only=True, validator=HelperValidationUtils.items_validator)
    """
    The data that describes a subscription item.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncreateitem
    """

    period: AdvancedCommercePeriod = AdvancedCommercePeriod.create_main_attr('rawPeriod', raw_required=True, kw_only=True)
    """
    The duration of a single cycle of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/period
    """

    rawPeriod: str = AdvancedCommercePeriod.create_raw_attr('period', required=True)
    """
    See period
    """

    taxCode: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A tax code that applies to a SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """

    previousTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A unique identifier that the App Store generates for a transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/transactionid
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
