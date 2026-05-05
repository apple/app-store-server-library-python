# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import List, Optional

from attr import define
import attr

from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .AdvancedCommerceRefund import AdvancedCommerceRefund

@define
class AdvancedCommerceTransactionItem:
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetransactionitem
    """

    SKU: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercesku
    """

    description: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedescription
    """

    displayName: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedisplayname
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceoffer
    """

    price: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceprice
    """

    refunds: Optional[List[AdvancedCommerceRefund]] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefunds
    """

    revocationDate: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/revocationdate
    """
