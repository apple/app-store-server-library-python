# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceDescriptors:
    """
    The display name and description of a subscription product.

    https://developer.apple.com/documentation/advancedcommerceapi/descriptors
    """

    description: str = attr.ib(kw_only=True, validator=HelperValidationUtils.description_validator)
    """
    A string that contains a description of the product.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(kw_only=True, validator=HelperValidationUtils.display_name_validator)
    """
    A string that contains the name of the product, suitable for display to customers.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """
