# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

@define
class AdvancedCommerceInfo:
    """
    A response object you provide to present an offer or switch-plan recommendation message.

    https://developer.apple.com/documentation/retentionmessaging/advancedcommerceinfo
    """

    messageIdentifier: Optional[UUID] = attr.ib(default=None)
    """
    The identifier of the message to display to the customer, along with the offer or switch-plan recommendation provided in advancedCommerceData.

    https://developer.apple.com/documentation/retentionmessaging/messageidentifier
    """

    advancedCommerceData: Optional[str] = attr.ib(default=None)
    """
    A Base64-encoded JSON object which contains a JWS describing an offer or switch-plan recommendation.

    https://developer.apple.com/documentation/retentionmessaging/advancedcommercedata
    """
