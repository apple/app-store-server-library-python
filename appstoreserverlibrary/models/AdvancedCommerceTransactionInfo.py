# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from .AdvancedCommercePeriod import AdvancedCommercePeriod
from .AdvancedCommerceTransactionItem import AdvancedCommerceTransactionItem
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceTransactionInfo(AttrsRawValueAware):
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetransactioninfo
    """

    descriptors: Optional[AdvancedCommerceDescriptors] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedescriptors
    """

    estimatedTax: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceestimatedtax
    """

    items: Optional[List[AdvancedCommerceTransactionItem]] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetransactionitems
    """

    period: Optional[AdvancedCommercePeriod] = AdvancedCommercePeriod.create_main_attr('rawPeriod', kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceperiod
    """

    rawPeriod: Optional[str] = AdvancedCommercePeriod.create_raw_attr('period')
    """
    See period
    """

    requestReferenceId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerequestreferenceid
    """

    taxCode: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetaxcode
    """

    taxExclusivePrice: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetaxexclusiveprice
    """

    taxRate: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetaxrate
    """
