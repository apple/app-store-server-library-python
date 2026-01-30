# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .AdvancedCommerceOneTimeChargeItem import AdvancedCommerceOneTimeChargeItem

@define
class AdvancedCommerceOneTimeChargeCreateRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request data your app provides when a customer purchases a one-time-charge product.

    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargecreaterequest
    """

    currency: str = attr.ib()
    """
    The currency of the price of the product.

    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    item: AdvancedCommerceOneTimeChargeItem = attr.ib()
    """
    The details of the product for purchase.

    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargeitem
    """

    taxCode: str = attr.ib()
    """
    The tax code for this product.

    https://developer.apple.com/documentation/advancedcommerceapi/taxCode
    """

    operation: str = attr.ib(init=False, default="CREATE_ONE_TIME_CHARGE", on_setattr=attr.setters.frozen)
    """
    The constant that represents the operation of this request.
    """

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)
    """
    The version number of the API.
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    The storefront for the transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """