# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AbstractAdvancedCommerceBaseItem import AbstractAdvancedCommerceBaseItem
from .AdvancedCommerceRefundReason import AdvancedCommerceRefundReason
from .AdvancedCommerceRefundType import AdvancedCommerceRefundType
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceRequestRefundItem(AbstractAdvancedCommerceBaseItem):
    """
    Information about the refund request for an item, such as its SKU, the refund amount, reason, and type.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """

    SKU: str = attr.ib(kw_only=True, validator=HelperValidationUtils.sku_validator)
    """
    The product identifier.

    https://developer.apple.com/documentation/advancedcommerceapi/sku
    """

    refundReason: AdvancedCommerceRefundReason = AdvancedCommerceRefundReason.create_main_attr('rawRefundReason', raw_required=True, kw_only=True)
    """
    The reason for the refund request.

    https://developer.apple.com/documentation/advancedcommerceapi/refundreason
    """

    rawRefundReason: str = AdvancedCommerceRefundReason.create_raw_attr('refundReason', required=True)
    """
    See refundReason
    """

    refundType: AdvancedCommerceRefundType = AdvancedCommerceRefundType.create_main_attr('rawRefundType', raw_required=True, kw_only=True)
    """
    The type of refund requested.

    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """

    rawRefundType: str = AdvancedCommerceRefundType.create_raw_attr('refundType', required=True)
    """
    See refundType
    """

    revoke: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/requestrefunditem
    """

    refundAmount: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The refund amount you’re requesting for the SKU, in milliunits of the currency.

    https://developer.apple.com/documentation/advancedcommerceapi/refundamount
    """
