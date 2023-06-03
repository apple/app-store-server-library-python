# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from appstoreserverlibrary.signed_data_verifier import VerificationStatus

@define
class LastTransactionsItem: 
    """
    The most recent App Store-signed transaction information and App Store-signed renewal information for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/lasttransactionsitem
    """

    status: VerificationStatus = attr.ib(default=None)
    """
    The status of the auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/status
    """

    originalTransactionId: str = attr.ib(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    signedTransactionInfo: str = attr.ib(default=None)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """

    signedRenewalInfo: str = attr.ib(default=None)
    """
    Subscription renewal information, signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo
    """