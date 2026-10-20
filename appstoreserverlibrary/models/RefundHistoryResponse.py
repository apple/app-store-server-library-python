# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

@define
class RefundHistoryResponse:
    """
    A response that contains an array of signed JSON Web Signature (JWS) refunded transactions, and paging information.

    https://developer.apple.com/documentation/appstoreserverapi/refundhistoryresponse
    """

    hasMore: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the App Store has more transactions than it returns in signedTransactions.

    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """

    revision: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A token you provide in a query to request the next set of transactions from the Get Refund History endpoint.

    https://developer.apple.com/documentation/appstoreserverapi/revision
    """

    signedTransactions: Optional[List[str]] = attr.ib(default=None, kw_only=True)
    """
    A list of up to 20 JWS transactions, or an empty array if the customer hasn’t received any refunds in your app.

    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """
