# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionMigrateItem(AbstractAdvancedCommerceItem):
    """
    The SKU, description, and display name to use for a migrated subscription item.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigrateitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The SKU to use for the migrated item.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    description: str = attr.ib(kw_only=True, validator=HelperValidationUtils.description_validator)
    """
    The description of the SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(kw_only=True, validator=HelperValidationUtils.display_name_validator)
    """
    The display name of the SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """
