# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .AdvancedCommerceOneTimeChargeItem import AdvancedCommerceOneTimeChargeItem
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceOneTimeChargeCreateRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request data your app provides when a customer purchases a one-time-charge product.

    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargecreaterequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata of the request.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    operation: str = attr.ib(init=False, default="CREATE_ONE_TIME_CHARGE", on_setattr=attr.setters.frozen)
    """
    The constant that represents the operation of this request.

    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargecreaterequest
    """

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)
    """
    The version number of the API.

    https://developer.apple.com/documentation/advancedcommerceapi/version
    """

    currency: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The currency of the price of the product.

    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    item: AdvancedCommerceOneTimeChargeItem = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The details of the product for purchase.

    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargeitem
    """

    taxCode: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The tax code for this product.

    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The storefront for the transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
