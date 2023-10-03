# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from appstoreserverlibrary.models.v2.Base import Model


class TransactionInfoResponse(Model):
    """
    A response that contains signed transaction information for a single transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactioninforesponse
    """

    signedTransactionInfo: Optional[str] = Field(default=None)
    """
    A customer’s in-app purchase transaction, signed by Apple, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """
