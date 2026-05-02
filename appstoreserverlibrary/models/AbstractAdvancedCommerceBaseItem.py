# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from abc import ABC

from attr import define
import attr

from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import AttrsRawValueAware

@define
class AbstractAdvancedCommerceBaseItem(AttrsRawValueAware, ABC):
    SKU: str = attr.ib(validator=HelperValidationUtils.sku_validator)
    """
    The product identifier of an in-app purchase product you manage in your own system.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """