# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
from typing import Optional
from uuid import UUID

from attr import define
import attr

from .BillingPlanType import BillingPlanType
from .LibraryUtility import AttrsRawValueAware

@define
class AlternateProduct(AttrsRawValueAware):
    """
    A switch-plan message and product ID you provide in a real-time response to your Get Retention Message endpoint.

    https://developer.apple.com/documentation/retentionmessaging/alternateproduct
    """

    messageIdentifier: Optional[UUID] = attr.ib(default=None)
    """
    The message identifier of the text to display in the switch-plan retention message.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The product identifier of the subscription the retention message suggests for your customer to switch to.

    https://developer.apple.com/documentation/retentionmessaging/productid
    """

    billingPlanType: Optional[BillingPlanType] = BillingPlanType.create_main_attr('rawBillingPlanType')
    """
    https://developer.apple.com/documentation/retentionmessaging/billingplantype
    """

    rawBillingPlanType: Optional[str] = BillingPlanType.create_raw_attr('billingPlanType')
    """
    See billingPlanType
    """
