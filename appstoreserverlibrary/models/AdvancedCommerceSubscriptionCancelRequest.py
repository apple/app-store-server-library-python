# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionCancelRequest(AdvancedCommerceRequest):
    """
    The request body for turning off automatic renewal of a subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptioncancelrequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
