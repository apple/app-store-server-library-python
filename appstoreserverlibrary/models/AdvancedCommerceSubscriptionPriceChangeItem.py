# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import attr
from attr import define
from typing import List, Optional  
from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionPriceChangeItem(AbstractAdvancedCommerceBaseItem):
    """
    The data your app provides to change a subscription price.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangeitem
    """

    price: int = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    dependentSKUs: Optional[List[str]] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.dependent_skus_validator))
    """
    https://developer.apple.com/documentation/advancedcommerceapi/dependentsku
    """