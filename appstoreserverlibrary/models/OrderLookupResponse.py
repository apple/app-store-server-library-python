# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
from typing import List, Optional
import attr

from .LibraryUtility import AttrsRawValueAware
from .OrderLookupStatus import OrderLookupStatus

@define
class OrderLookupResponse(AttrsRawValueAware):
    """
    A response that includes the order lookup status and an array of signed transactions for the in-app purchases in the order.
    
    https://developer.apple.com/documentation/appstoreserverapi/orderlookupresponse
    """

    status: Optional[OrderLookupStatus] = OrderLookupStatus.create_main_attr('rawStatus')
    """
    The status that indicates whether the order ID is valid.
    
    https://developer.apple.com/documentation/appstoreserverapi/orderlookupstatus
    """

    rawStatus: Optional[int] = OrderLookupStatus.create_raw_attr('status')
    """
    See status
    """

    signedTransactions: Optional[List[str]] = attr.ib(default=None)
    """
    An array of in-app purchase transactions that are part of order, signed by Apple, in JSON Web Signature format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """
