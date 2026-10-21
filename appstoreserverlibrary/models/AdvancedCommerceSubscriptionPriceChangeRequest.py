# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceSubscriptionPriceChangeItem import AdvancedCommerceSubscriptionPriceChangeItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionPriceChangeRequest(AdvancedCommerceRequest):
    """
    The request body you use to change the price of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangerequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    Metadata that identifies the request.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    items: List[AdvancedCommerceSubscriptionPriceChangeItem] = attr.ib(kw_only=True, validator=HelperValidationUtils.items_validator)
    """
    An array that contains one or more SKUs and the changed price for each SKU.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionpricechangeitem
    """

    currency: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The currency of the prices.

    https://developer.apple.com/documentation/advancedcommerceapi/currency
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The App Store storefront of the subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
