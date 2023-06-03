# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr

@define
class TransactionInfoResponse:
    """
    A response that contains signed transaction information for a single transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactioninforesponse
    """
    
    signedTransactionInfo: str = attr.ib(default=None)
    """
    A customer’s in-app purchase transaction, signed by Apple, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """
