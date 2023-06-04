# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .Environment import Environment

@define
class AppTransaction: 
    """
    Information that represents the customer’s purchase of the app, cryptographically signed by the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction
    """

    receiptType: Environment = attr.ib(default=None)
    """
    The server environment that signs the app transaction.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3963901-environment
    """

    appAppleId: int = attr.ib(default=None)
    """
    The unique identifier the App Store uses to identify the app.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954436-appid
    """

    bundleId: str = attr.ib(default=None)
    """
    The bundle identifier that the app transaction applies to.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954439-bundleid
    """

    applicationVersion: str = attr.ib(default=None)
    """
    The app version that the app transaction applies to.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954437-appversion
    """

    versionExternalIdentifier: int = attr.ib(default=None)
    """
    The version external identifier of the app
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954438-appversionid
    """

    receiptCreationDate: int = attr.ib(default=None)
    """
    The date that the App Store signed the JWS app transaction.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954449-signeddate
    """

    originalPurchaseDate: int = attr.ib(default=None)
    """
    The date the user originally purchased the app from the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954448-originalpurchasedate
    """

    originalApplicationVersion: str = attr.ib(default=None)
    """
    The app version that the user originally purchased from the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954447-originalappversion
    """

    deviceVerification: str = attr.ib(default=None)
    """
    The Base64 device verification value to use to verify whether the app transaction belongs to the device.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954441-deviceverification
    """

    deviceVerificationNonce: str = attr.ib(default=None)
    """
    The UUID used to compute the device verification value.
    
    https://developer.apple.com/documentation/storekit/apptransaction/3954442-deviceverificationnonce
    """

    preorderDate: int = attr.ib(default=None)
    """
    The date the customer placed an order for the app before it's available in the App Store.
    
    https://developer.apple.com/documentation/storekit/apptransaction/4013175-preorderdate
    """