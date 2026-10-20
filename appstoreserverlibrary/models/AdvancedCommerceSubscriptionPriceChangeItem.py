# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionPriceChangeItem(AbstractAdvancedCommerceBaseItem):
    """
    The data your app provides to change a subscription price.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangeitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The product identifier of an Apple In-App Purchase product you manage in your own system.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    price: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A price, in milliunits of a currency, for an Advanced Commerce API SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    dependentSKUs: Optional[List[str]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.dependent_skus_validator))
    """
    The product identifier of a dependent SKU in a subscription price change.

    https://developer.apple.com/documentation/advancedcommerceapi/dependentsku
    """
