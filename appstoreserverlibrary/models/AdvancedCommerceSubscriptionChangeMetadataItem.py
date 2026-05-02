# Copyright (c) 2026 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionChangeMetadataItem():
    """
    The metadata to change for an item, specifically its SKU, description, and display name.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadataitem
    """

    currentSKU: str = attr.ib(validator=HelperValidationUtils.sku_validator)
    """
    The original SKU of the item.
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

    description: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.description_validator))
    """
    The new description for the item.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.display_name_validator))
    """
    The new display name for the item.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """   
    
    SKU: Optional[str] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.sku_validator))
    """
    The new SKU of the item.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """