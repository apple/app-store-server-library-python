# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import List, Optional

from attr import define
import attr

from .AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from .AdvancedCommercePeriod import AdvancedCommercePeriod
from .AdvancedCommerceRenewalItem import AdvancedCommerceRenewalItem
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceRenewalInfo(AttrsRawValueAware):
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerenewalinfo
    """

    consistencyToken: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceconsistencytoken
    """

    descriptors: Optional[AdvancedCommerceDescriptors] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercedescriptors
    """

    items: Optional[List[AdvancedCommerceRenewalItem]] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerenewalitem
    """

    period: Optional[AdvancedCommercePeriod] = AdvancedCommercePeriod.create_main_attr('rawPeriod')
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommerceperiod
    """

    rawPeriod: Optional[str] = AdvancedCommercePeriod.create_raw_attr('period')
    """
    See period
    """

    requestReferenceId: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerequestreferenceid
    """

    taxCode: Optional[str] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetaxcode
    """
