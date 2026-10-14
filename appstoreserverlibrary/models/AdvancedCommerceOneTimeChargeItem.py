# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceOneTimeChargeItem(AbstractAdvancedCommerceItem):
    """
    The details of a one-time charge product, including its display name, price, SKU, and metadata.

    https://developer.apple.com/documentation/advancedcommerceapi/onetimechargeitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The product identifier.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    description: str = attr.ib(kw_only=True, validator=HelperValidationUtils.description_validator)
    """
    A description of the product that doesn’t display to customers.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(kw_only=True, validator=HelperValidationUtils.display_name_validator)
    """
    The product name, suitable for display to customers.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """

    price: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The price, in milliunits of the currency, of the one-time charge product.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """
