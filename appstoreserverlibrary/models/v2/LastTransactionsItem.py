# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from appstoreserverlibrary.models.Status import Status
from appstoreserverlibrary.models.v2.Base import Model


class LastTransactionsItem(Model):
    """
    The most recent App Store-signed transaction information and App Store-signed renewal information for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/lasttransactionsitem
    """

    status: Optional[Status] = Field(default=None)
    """
    The status of the auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/status
    """

    originalTransactionId: Optional[str] = Field(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    signedTransactionInfo: Optional[str] = Field(default=None)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """

    signedRenewalInfo: Optional[str] = Field(default=None)
    """
    Subscription renewal information, signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo
    """
