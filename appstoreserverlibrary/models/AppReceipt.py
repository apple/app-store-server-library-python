# Copyright (c) 2026 Apple Inc. Licensed under MIT License.
from typing import Dict, List, Optional

from attr import define
import attr

from .InAppPurchaseReceipt import InAppPurchaseReceipt

@define
class AppReceipt:
    """
    A decoded legacy App Store receipt (the PKCS#7 app receipt).

    https://developer.apple.com/documentation/appstorereceipts/responsebody/receipt
    """

    receiptType: Optional[str] = attr.ib(default=None)
    """
    The raw receipt type, e.g. Production, ProductionVPP, ProductionSandbox, ProductionVPPSandbox or Xcode.
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of the app the receipt belongs to.

    https://developer.apple.com/documentation/appstorereceipts/bundle_id
    """

    bundleIdBytes: Optional[bytes] = attr.ib(default=None)
    """
    The raw ASN.1 bytes of the bundle identifier attribute, needed together with opaqueValue and sha1Hash
    to compute the device-hash binding described in Apple's receipt validation guide.
    """

    applicationVersion: Optional[str] = attr.ib(default=None)
    """
    The app's version number.

    https://developer.apple.com/documentation/appstorereceipts/application_version
    """

    opaqueValue: Optional[bytes] = attr.ib(default=None)
    """
    An opaque value used, with other data, to compute the device hash.
    """

    sha1Hash: Optional[bytes] = attr.ib(default=None)
    """
    The SHA-1 device-hash attribute of the receipt.
    """

    receiptCreationDate: Optional[int] = attr.ib(default=None)
    """
    The time the App Store generated the receipt, in UNIX time, in milliseconds.

    https://developer.apple.com/documentation/appstorereceipts/receipt_creation_date
    """

    originalPurchaseDate: Optional[int] = attr.ib(default=None)
    """
    The time of the original app purchase, in UNIX time, in milliseconds.

    https://developer.apple.com/documentation/appstorereceipts/original_purchase_date
    """

    originalApplicationVersion: Optional[str] = attr.ib(default=None)
    """
    The version of the app that the user originally purchased.

    https://developer.apple.com/documentation/appstorereceipts/original_application_version
    """

    expirationDate: Optional[int] = attr.ib(default=None)
    """
    The expiration date of the receipt, in UNIX time, in milliseconds. Present for apps purchased through the
    Volume Purchase Program.

    https://developer.apple.com/documentation/appstorereceipts/expiration_date
    """

    inAppPurchases: Optional[List[InAppPurchaseReceipt]] = attr.ib(default=None)
    """
    The decoded in-app purchase attributes contained in the receipt.

    https://developer.apple.com/documentation/appstorereceipts/responsebody/receipt/in_app
    """

    unknownAttributes: Optional[Dict[int, List[bytes]]] = attr.ib(default=None)
    """
    Attribute types this library does not model, keyed by type, with the verified-but-undecoded value bytes,
    so fields Apple adds later remain accessible without a library update.
    """
