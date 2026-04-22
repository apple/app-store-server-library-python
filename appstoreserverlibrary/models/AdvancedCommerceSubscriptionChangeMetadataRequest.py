# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceSubscriptionChangeMetadataDescriptors import AdvancedCommerceSubscriptionChangeMetadataDescriptors
from .AdvancedCommerceSubscriptionChangeMetadataItem import AdvancedCommerceSubscriptionChangeMetadataItem
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils

@define
class AdvancedCommerceSubscriptionChangeMetadataRequest(AdvancedCommerceRequest):
    """
    The request body you provide to change the metadata of a subscription.
    
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadatarequest
    """

    descriptors: Optional[AdvancedCommerceSubscriptionChangeMetadataDescriptors] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadatadescriptors
    """

    items: Optional[List[AdvancedCommerceSubscriptionChangeMetadataItem]] = attr.ib(default=None, validator=attr.validators.optional(AdvancedCommerceValidationUtils.items_validator))
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionchangemetadataitem
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """

    taxCode: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/taxcode
    """