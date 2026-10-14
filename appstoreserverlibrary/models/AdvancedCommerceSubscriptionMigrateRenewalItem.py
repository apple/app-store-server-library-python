# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AbstractAdvancedCommerceItem import AbstractAdvancedCommerceItem
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionMigrateRenewalItem(AbstractAdvancedCommerceItem):
    """
    The item information that replaces a migrated subscription item when the subscription renews.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigraterenewalitem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The SKU that the subscription item renews to at the next renewal period.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    description: str = attr.ib(kw_only=True, validator=HelperValidationUtils.description_validator)
    """
    The description of the renewing SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(kw_only=True, validator=HelperValidationUtils.display_name_validator)
    """
    The display name of the renewing SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """
