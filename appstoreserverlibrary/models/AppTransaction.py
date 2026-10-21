# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware
from .PurchasePlatform import PurchasePlatform
from .StoreType import StoreType

@define
class AppTransaction(AttrsRawValueAware):
    """
    A decoded payload that contains app transaction information.

    https://developer.apple.com/documentation/storekit/apptransaction
    https://developer.apple.com/documentation/appstoreserverapi/jwsapptransactiondecodedpayload
    """

    appAppleId: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier the App Store uses to identify the app.

    https://developer.apple.com/documentation/appstoreserverapi/appappleid
    """

    appTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the app download transaction.

    https://developer.apple.com/documentation/appstoreserverapi/apptransactionid
    """

    bundleId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The bundle identifier that the app transaction applies to.

    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    originalApplicationVersion: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The app version that the customer originally purchased from the App Store.

    https://developer.apple.com/documentation/appstoreserverapi/originalapplicationversion
    """

    originalPlatform: Optional[PurchasePlatform] = PurchasePlatform.create_main_attr('rawOriginalPlatform', kw_only=True)
    """
    The platform on which the customer originally purchased the app.

    https://developer.apple.com/documentation/appstoreserverapi/originalplatform
    """

    rawOriginalPlatform: Optional[str] = PurchasePlatform.create_raw_attr('originalPlatform')
    """
    See originalPlatform
    """

    originalPurchaseDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The date the customer originally purchased the app from the App Store.

    https://developer.apple.com/documentation/appstoreserverapi/originalpurchasedate
    """

    preorderDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The date the customer placed an order for the app before it’s available in the App Store.

    https://developer.apple.com/documentation/appstoreserverapi/preorderdate
    """

    receiptCreationDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The date that the App Store signed the JWS app transaction.

    https://developer.apple.com/documentation/appstoreserverapi/receiptcreationdate
    """

    receiptType: Optional[Environment] = Environment.create_main_attr('rawReceiptType', kw_only=True)
    """
    The server environment, production or sandbox, that signed the app transaction.

    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    rawReceiptType: Optional[str] = Environment.create_raw_attr('receiptType')
    """
    See receiptType
    """

    storeType: Optional[StoreType] = StoreType.create_main_attr('rawStoreType', kw_only=True)
    """
    The store the customer obtained the app from.

    https://developer.apple.com/documentation/appstoreserverapi/storetype
    """

    rawStoreType: Optional[str] = StoreType.create_raw_attr('storeType')
    """
    See storeType
    """

    applicationVersion: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The app version that the app transaction applies to.

    https://developer.apple.com/documentation/storekit/apptransaction/appversion
    """

    versionExternalIdentifier: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The number that the App Store uses to uniquely identify the version of the app.

    https://developer.apple.com/documentation/storekit/apptransaction/appversionid
    """

    deviceVerification: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The device verification value to use to verify whether the app transaction belongs to the device.

    https://developer.apple.com/documentation/storekit/apptransaction/deviceverification
    """

    deviceVerificationNonce: Optional[UUID] = attr.ib(default=None, kw_only=True)
    """
    The UUID used to compute the device verification value.

    https://developer.apple.com/documentation/storekit/apptransaction/deviceverificationnonce
    """
