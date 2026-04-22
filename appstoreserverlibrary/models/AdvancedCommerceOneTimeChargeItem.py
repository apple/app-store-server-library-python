# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem

@define
class AdvancedCommerceOneTimeChargeItem(AbstractAdvancedCommerceItem):
    """
    The details of a one-time charge product, including its display name, price, SKU, and metadata.
    
    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargeitem
    """

    price: int = attr.ib()
    """
    The price, in milliunits of the currency, of the one-time charge product.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """