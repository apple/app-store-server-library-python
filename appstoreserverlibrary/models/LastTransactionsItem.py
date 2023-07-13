# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from appstoreserverlibrary.models.Status import Status

@define
class LastTransactionsItem: 
    """
    The most recent App Store-signed transaction information and App Store-signed renewal information for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/lasttransactionsitem
    """

    status: Optional[Status] = attr.ib(default=None)
    """
    The status of the auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/status
    """

    originalTransactionId: Optional[str] = attr.ib(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    signedTransactionInfo: Optional[str] = attr.ib(default=None)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """

    signedRenewalInfo: Optional[str] = attr.ib(default=None)
    """
    Subscription renewal information, signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo
    """