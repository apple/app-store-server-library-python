# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .AdvancedCommercePriceIncreaseInfoStatus import AdvancedCommercePriceIncreaseInfoStatus
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommercePriceIncreaseInfo(AttrsRawValueAware):
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercepriceincreaseinfo
    """

    dependentSKUs: Optional[List[str]] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercepriceincreaseinfodependentsku
    """

    price: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercepriceincreaseinfoprice
    """

    status: Optional[AdvancedCommercePriceIncreaseInfoStatus] = AdvancedCommercePriceIncreaseInfoStatus.create_main_attr('rawStatus', kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercepriceincreaseinfostatus
    """

    rawStatus: Optional[str] = AdvancedCommercePriceIncreaseInfoStatus.create_raw_attr('status')
    """
    See status
    """
