# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceSubscriptionMigrateDescriptors import AdvancedCommerceSubscriptionMigrateDescriptors
from .AdvancedCommerceSubscriptionMigrateItem import AdvancedCommerceSubscriptionMigrateItem
from .AdvancedCommerceSubscriptionMigrateRenewalItem import AdvancedCommerceSubscriptionMigrateRenewalItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionMigrateRequest(AdvancedCommerceRequest):
    """
    The subscription details you provide to migrate a subscription from Apple In-App Purchase to the Advanced Commerce API, such as descriptors, items, storefront, and more.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigraterequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    descriptors: AdvancedCommerceSubscriptionMigrateDescriptors = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The description and display name of the subscription to migrate to that you manage.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigratedescriptors
    """

    items: List[AdvancedCommerceSubscriptionMigrateItem] = attr.ib(kw_only=True, validator=HelperValidationUtils.items_validator)
    """
    An array of one or more SKUs, along with descriptions and display names, that are included in the subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigrateitem
    """

    targetProductId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    Your generic product ID for an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/targetproductid
    """

    taxCode: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A tax code that applies to a SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """

    renewalItems: Optional[List[AdvancedCommerceSubscriptionMigrateRenewalItem]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    An optional array of subscription items that represents the items that renew at the next renewal period, if they differ from items.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigraterenewalitem
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
