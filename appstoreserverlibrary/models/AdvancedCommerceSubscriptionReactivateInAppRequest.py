# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AbstractAdvancedCommerceInAppRequest import AbstractAdvancedCommerceInAppRequest
from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .AdvancedCommerceSubscriptionReactivateItem import AdvancedCommerceSubscriptionReactivateItem
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceSubscriptionReactivateInAppRequest(AbstractAdvancedCommerceInAppRequest):
    """
    The request your app provides to reactivate a subscription that has automatic renewal turned off.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateinapprequest
    """

    requestInfo: AdvancedCommerceRequestInfo = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    operation: str = attr.ib(init=False, default="REACTIVATE_SUBSCRIPTION", on_setattr=attr.setters.frozen)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateinapprequest
    """

    version: str = attr.ib(init=False, default="1", on_setattr=attr.setters.frozen)
    """
    A number that represents the version of the data structure or Advanced Commerce API.

    https://developer.apple.com/documentation/advancedcommerceapi/version
    """

    transactionId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A unique identifier that the App Store generates for a transaction.

    https://developer.apple.com/documentation/advancedcommerceapi/transactionid
    """

    items: Optional[List[AdvancedCommerceSubscriptionReactivateItem]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(HelperValidationUtils.items_validator))
    """
    An item in a subscription to reactivate.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionreactivateitem
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A three-letter code that represents the country or region associated with the App Store storefront.

    https://developer.apple.com/documentation/advancedcommerceapi/storefront
    """
