# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List
import attr
from attr import define
from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils
from .AdvancedCommerceSubscriptionMigrateDescriptors import AdvancedCommerceSubscriptionMigrateDescriptors
from .AdvancedCommerceSubscriptionMigrateItem import AdvancedCommerceSubscriptionMigrateItem
from .AdvancedCommerceSubscriptionMigrateRenewalItem import AdvancedCommerceSubscriptionMigrateRenewalItem

@define
class AdvancedCommerceSubscriptionMigrateRequest(AdvancedCommerceRequest):
    """
    The subscription details you provide to migrate a subscription from In-App Purchase to the Advanced Commerce API, such as descriptors, items, storefront, and more.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigraterequest
    """

    descriptors: AdvancedCommerceSubscriptionMigrateDescriptors = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigratedescriptors
    """

    items: List[AdvancedCommerceSubscriptionMigrateItem] = attr.ib(validator=AdvancedCommerceValidationUtils.items_validator)
    """
    An array of one or more SKUs, along with descriptions and display names, that are included in the subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigrateitem
    """

    targetProductId: str = attr.ib()
    """
    Your generic product ID for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/targetproductid
    """

    taxCode: str = attr.ib()
    """
    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """

    renewalItems: Optional[List[AdvancedCommerceSubscriptionMigrateRenewalItem]] = attr.ib(default=None, validator=attr.validators.optional(AdvancedCommerceValidationUtils.items_validator))
    """
    An optional array of subscription items that represents the items that renew at the next renewal period, if they differ from items.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigraterenewalitem
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """