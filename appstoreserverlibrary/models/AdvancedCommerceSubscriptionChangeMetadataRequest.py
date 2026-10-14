# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceSubscriptionChangeMetadataDescriptors import AdvancedCommerceSubscriptionChangeMetadataDescriptors
from .AdvancedCommerceSubscriptionChangeMetadataItem import AdvancedCommerceSubscriptionChangeMetadataItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionChangeMetadataRequest(AdvancedCommerceRequest):
    """
    The request body you provide to change the metadata of a subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadatarequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    descriptors: Optional[AdvancedCommerceSubscriptionChangeMetadataDescriptors] = attr.ib(default=None, kw_only=True)
    """
    The subscription metadata to change, specifically the description and display name.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadatadescriptors
    """

    items: Optional[List[AdvancedCommerceSubscriptionChangeMetadataItem]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    The metadata to change for an item, specifically its SKU, description, and display name.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadataitem
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """

    taxCode: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A tax code that applies to a SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """
