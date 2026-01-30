# Copyright (c) 2026 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils

@define
class AdvancedCommerceSubscriptionChangeMetadataDescriptors():
    """
    The subscription metadata to change, specifically the description and display name.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadatadescriptors
    """

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True)
    """
    The string that determines when the metadata change goes into effect.
    
    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    description: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(AdvancedCommerceValidationUtils.description_validator)
    )
    """
    The new description for the subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(AdvancedCommerceValidationUtils.display_name_validator)
    )
    """
    The new display name for the subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """