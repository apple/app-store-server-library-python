# Copyright (c) 2026 Apple Inc. Licensed under MIT License.
from typing import Dict, List, Optional

from attr import define
import attr

@define
class InAppPurchaseReceipt:
    """
    A decoded in-app purchase attribute from a legacy App Store receipt.

    https://developer.apple.com/documentation/appstorereceipts/responsebody/receipt/in_app
    """

    quantity: Optional[int] = attr.ib(default=None)
    """
    The number of items purchased.

    https://developer.apple.com/documentation/appstorereceipts/quantity
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of the product purchased.

    https://developer.apple.com/documentation/appstorereceipts/product_id
    """

    transactionId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of the transaction.

    https://developer.apple.com/documentation/appstorereceipts/transaction_id
    """

    originalTransactionId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of the original transaction.

    https://developer.apple.com/documentation/appstorereceipts/original_transaction_id
    """

    purchaseDate: Optional[int] = attr.ib(default=None)
    """
    The time of the purchase, in UNIX time, in milliseconds.

    https://developer.apple.com/documentation/appstorereceipts/purchase_date
    """

    originalPurchaseDate: Optional[int] = attr.ib(default=None)
    """
    The time of the original purchase, in UNIX time, in milliseconds.

    https://developer.apple.com/documentation/appstorereceipts/original_purchase_date
    """

    expiresDate: Optional[int] = attr.ib(default=None)
    """
    The expiration time of the subscription, in UNIX time, in milliseconds.

    https://developer.apple.com/documentation/appstorereceipts/expires_date
    """

    cancellationDate: Optional[int] = attr.ib(default=None)
    """
    The time Apple customer support canceled the transaction or the subscription was upgraded, in UNIX time, in milliseconds.

    https://developer.apple.com/documentation/appstorereceipts/cancellation_date
    """

    webOrderLineItemId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of subscription purchase events across devices, including subscription renewals.

    https://developer.apple.com/documentation/appstorereceipts/web_order_line_item_id
    """

    isInIntroOfferPeriod: Optional[bool] = attr.ib(default=None)
    """
    Whether the subscription is in an introductory offer period.

    https://developer.apple.com/documentation/appstorereceipts/is_in_intro_offer_period
    """

    unknownAttributes: Optional[Dict[int, List[bytes]]] = attr.ib(default=None)
    """
    Attribute types this library does not model, keyed by type, with the verified-but-undecoded value bytes,
    so fields Apple adds later remain accessible without a library update.
    """
