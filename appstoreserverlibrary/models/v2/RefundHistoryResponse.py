# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
from typing import List, Optional
import attr
from pydantic import Field

from appstoreserverlibrary.models.v2.Base import Model


class RefundHistoryResponse(Model):
    """
    A response that contains an array of signed JSON Web Signature (JWS) refunded transactions, and paging information.
    
    https://developer.apple.com/documentation/appstoreserverapi/refundhistoryresponse
    """

    signedTransactions: Optional[List[str]] = Field(default=None)
    """
    A list of up to 20 JWS transactions, or an empty array if the customer hasn't received any refunds in your app. The transactions are sorted in ascending order by revocationDate.
    """

    revision: Optional[str] = Field(default=None)
    """
    A token you use in a query to request the next set of transactions for the customer.
    
    https://developer.apple.com/documentation/appstoreserverapi/revision
    """

    hasMore: Optional[bool] = Field(default=None)
    """
    A Boolean value indicating whether the App Store has more transaction data.
    
    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """
