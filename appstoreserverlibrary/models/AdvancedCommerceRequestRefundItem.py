# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem
from .AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from .AdvancedCommerceRefundType import AdvancedCommerceRefundType

@define
class AdvancedCommerceRequestRefundItem(AbstractAdvancedCommerceBaseItem):
    """
    Information about the refund request for an item, such as its SKU, the refund amount, reason, and type.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """

    revoke: bool = attr.ib()

    refundReason: AdvancedCommerceRefundReason = AdvancedCommerceRefundReason.create_main_attr('rawRefundReason', raw_required=True)
    """
    The reason for the refund request.

    https://developer.apple.com/documentation/advancedcommerceapi/refundreason
    """

    rawRefundReason: str = AdvancedCommerceRefundReason.create_raw_attr('refundReason', required=True)
    """
    See refundReason
    """

    refundType: AdvancedCommerceRefundType = AdvancedCommerceRefundType.create_main_attr('rawRefundType', raw_required=True)
    """
    The type of refund requested.
    """

    rawRefundType: str = AdvancedCommerceRefundType.create_raw_attr('refundType', required=True)
    """
    See refundType
    """

    refundAmount: Optional[int] = attr.ib(default=None)
    """
    The refund amount you're requesting for the SKU, in milliunits of the currency.

    https://developer.apple.com/documentation/advancedcommerceapi/refundamount
    """