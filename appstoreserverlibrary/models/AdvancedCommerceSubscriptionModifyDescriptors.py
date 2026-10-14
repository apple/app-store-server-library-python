# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceSubscriptionModifyDescriptors(AttrsRawValueAware):
    """
    The data your app provides to change the description and display name of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifydescriptors
    """

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True, kw_only=True)
    """
    A string value that indicates when a requested change to an auto-renewable subscription goes into effect.

    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    description: Optional[str] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.description_validator))
    """
    A string you provide that describes a SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: Optional[str] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.display_name_validator))
    """
    A string with a product name that you can localize and is suitable for display to customers.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """
