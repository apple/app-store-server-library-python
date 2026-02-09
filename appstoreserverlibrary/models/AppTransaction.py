# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware

from .Environment import Environment
from .PurchasePlatform import PurchasePlatform

@define
class AppTransaction(AttrsRawValueAware):
    """
    Information that represents the customer’s purchase of the app, cryptographically signed by the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction
    """

    receiptType: Optional[Environment] = Environment.create_main_attr('rawReceiptType')
    """
    The server environment that signs the app transaction.
    
    https://developer.apple.com/documentation/storekit/apptransaction/environment
    """

    rawReceiptType: Optional[str] = Environment.create_raw_attr('receiptType')
    """
    See receiptType
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier the App Store uses to identify the app.
    
    https://developer.apple.com/documentation/storekit/apptransaction/appid
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier that the app transaction applies to.
    
    https://developer.apple.com/documentation/storekit/apptransaction/bundleid
    """

    applicationVersion: Optional[str] = attr.ib(default=None)
    """
    The app version that the app transaction applies to.
    
    https://developer.apple.com/documentation/storekit/apptransaction/appversion
    """

    versionExternalIdentifier: Optional[int] = attr.ib(default=None)
    """
    The version external identifier of the app
    
    https://developer.apple.com/documentation/storekit/apptransaction/appversionid
    """

    receiptCreationDate: Optional[int] = attr.ib(default=None)
    """
    The date that the App Store signed the JWS app transaction.
    
    https://developer.apple.com/documentation/storekit/apptransaction/signeddate
    """

    originalPurchaseDate: Optional[int] = attr.ib(default=None)
    """
    The date the user originally purchased the app from the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction/originalpurchasedate
    """

    originalApplicationVersion: Optional[str] = attr.ib(default=None)
    """
    The app version that the user originally purchased from the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction/originalappversion
    """

    deviceVerification: Optional[str] = attr.ib(default=None)
    """
    The Base64 device verification value to use to verify whether the app transaction belongs to the device.
    
    https://developer.apple.com/documentation/storekit/apptransaction/deviceverification
    """

    deviceVerificationNonce: Optional[str] = attr.ib(default=None)
    """
    The UUID used to compute the device verification value.
    
    https://developer.apple.com/documentation/storekit/apptransaction/deviceverificationnonce
    """

    preorderDate: Optional[int] = attr.ib(default=None)
    """
    The date the customer placed an order for the app before it's available in the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction/preorderdate
    """

    appTransactionId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of the app download transaction.
    
    https://developer.apple.com/documentation/storekit/apptransaction/apptransactionid
    """

    originalPlatform: Optional[PurchasePlatform] = PurchasePlatform.create_main_attr('rawOriginalPlatform')
    """
    The platform on which the customer originally purchased the app.
    
    https://developer.apple.com/documentation/storekit/apptransaction/originalplatform
    """

    rawOriginalPlatform: Optional[str] = PurchasePlatform.create_raw_attr('originalPlatform')
    """
    See originalPlatform
    """
