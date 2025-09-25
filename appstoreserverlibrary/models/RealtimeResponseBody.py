# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, Dict, Any
from attr import define
import attr
from .Message import Message
from .AlternateProduct import AlternateProduct
from .PromotionalOffer import PromotionalOffer

@define
class RealtimeResponseBody:
    """
    A response you provide to choose, in real time, a retention message the system displays to the customer.

    Note: The fields in RealtimeResponseBody are mutually exclusive. Choose the type of retention message
    to display, and respond using only the field that represents that message type.

    https://developer.apple.com/documentation/retentionmessaging/realtimeresponsebody
    """

    message: Optional[Message] = attr.ib(default=None)
    """
    A retention message that's text-based and can include an optional image.
    If you supply this field, don't include the other fields.

    https://developer.apple.com/documentation/retentionmessaging/message
    """

    alternateProduct: Optional[AlternateProduct] = attr.ib(default=None)
    """
    A retention message with a switch-plan option.
    If you supply this field, don't include the other fields.

    https://developer.apple.com/documentation/retentionmessaging/alternateproduct
    """

    promotionalOffer: Optional[PromotionalOffer] = attr.ib(default=None)
    """
    A retention message that includes a promotional offer.
    If you supply this field, don't include the other fields.

    https://developer.apple.com/documentation/retentionmessaging/promotionaloffer
    """

    def to_json_dict(self) -> Dict[str, Any]:
        """
        Convert to a dictionary suitable for JSON serialization.
        Omits None values to maintain mutual exclusivity of fields.

        Example:
            response = RealtimeResponseBody(
                message=Message(messageIdentifier="msg123")
            )
            json_data = json.dumps(response.to_json_dict())
            # Result: {"message": {"messageIdentifier": "msg123"}}

        :return: Dictionary representation suitable for JSON encoding
        """
        from .LibraryUtility import _get_retention_response_converter
        converter = _get_retention_response_converter()
        return converter.unstructure(self)