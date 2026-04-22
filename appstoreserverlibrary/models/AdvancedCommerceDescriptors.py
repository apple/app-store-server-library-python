# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils

@define
class AdvancedCommerceDescriptors:
    """
    The display name and description of a subscription product.

    https://developer.apple.com/documentation/advancedcommerceapi/descriptors
    """
    description: str = attr.ib(validator=AdvancedCommerceValidationUtils.description_validator)
    """
    A string you provide that describes a SKU.
    
    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(validator=AdvancedCommerceValidationUtils.display_name_validator)
    """
    A string with a product name that you can localize and is suitable for display to customers.
    
    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """