# Copyright (c) 2026 Apple Inc. Licensed under MIT License.
from typing import Optional

import attr
from attr import define
from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils

@define
class AdvancedCommerceSubscriptionModifyDescriptors():
    """
    The data your app provides to change the description and display name of an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifydescriptors
    """

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    description: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(AdvancedCommerceValidationUtils.description_validator))
    """
    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(AdvancedCommerceValidationUtils.display_name_validator)
    )
    """
    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """