# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import List, Optional

from pydantic import Field

from .Base import Model
from .OrderLookupStatus import OrderLookupStatus


class OrderLookupResponse(Model):
    """
    A response that includes the order lookup status and an array of signed transactions for the in-app purchases in the order.
    
    https://developer.apple.com/documentation/appstoreserverapi/orderlookupresponse
    """

    status: Optional[OrderLookupStatus] = Field(default=None)
    """
    The status that indicates whether the order ID is valid.
    
    https://developer.apple.com/documentation/appstoreserverapi/orderlookupstatus
    """

    signedTransactions: Optional[List[str]] = Field(default=None)
    """
    An array of in-app purchase transactions that are part of order, signed by Apple, in JSON Web Signature format.
    """
