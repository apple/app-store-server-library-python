# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceOffer import AdvancedCommerceOffer
from .AdvancedCommerceRefund import AdvancedCommerceRefund

@define
class AdvancedCommerceTransactionItem:
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetransactionitem
    """

    SKU: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercesku
    """

    description: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedescription
    """

    displayName: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedisplayname
    """

    offer: Optional[AdvancedCommerceOffer] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceoffer
    """

    price: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceprice
    """

    refunds: Optional[List[AdvancedCommerceRefund]] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefunds
    """

    revocationDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that the App Store refunded the transaction or revoked it from Family Sharing.

    https://developer.apple.com/documentation/appstoreserverapi/revocationdate
    """
