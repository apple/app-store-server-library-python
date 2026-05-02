# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from .AdvancedCommerceRefundType import AdvancedCommerceRefundType
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceRefund(AttrsRawValueAware):
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefund
    """

    refundAmount: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefundamount
    """

    refundDate: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefunddate
    """

    refundReason: Optional[AdvancedCommerceRefundReason] = AdvancedCommerceRefundReason.create_main_attr('rawRefundReason')
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefundreason
    """

    rawRefundReason: Optional[str] = AdvancedCommerceRefundReason.create_raw_attr('refundReason')
    """
    See refundReason
    """

    refundType: Optional[AdvancedCommerceRefundType] = AdvancedCommerceRefundType.create_main_attr('rawRefundType')
    """
    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerefundtype
    """

    rawRefundType: Optional[str] = AdvancedCommerceRefundType.create_raw_attr('refundType')
    """
    See refundType
    """
