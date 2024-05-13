# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .OfferDiscountType import OfferDiscountType
from .Environment import Environment
from .InAppOwnershipType import InAppOwnershipType
from .LibraryUtility import AttrsRawValueAware
from .OfferType import OfferType
from .RevocationReason import RevocationReason
from .TransactionReason import TransactionReason

from .Type import Type

@define
class JWSTransactionDecodedPayload(AttrsRawValueAware):
    """
    A decoded payload containing transaction information.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransactiondecodedpayload
    """

    originalTransactionId: Optional[str] = attr.ib(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    transactionId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier for a transaction such as an in-app purchase, restored in-app purchase, or subscription renewal.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionid
    """

    webOrderLineItemId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of subscription-purchase events across devices, including renewals.
    
    https://developer.apple.com/documentation/appstoreserverapi/weborderlineitemid
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """    

    subscriptionGroupIdentifier: Optional[str] = attr.ib(default=None)
    """
    The identifier of the subscription group that the subscription belongs to.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifier
    """

    purchaseDate: Optional[int] = attr.ib(default=None)
    """
    The time that the App Store charged the user's account for an in-app purchase, a restored in-app purchase, a subscription, or a subscription renewal after a lapse.
    
    https://developer.apple.com/documentation/appstoreserverapi/purchasedate
    """

    originalPurchaseDate: Optional[int] = attr.ib(default=None)
    """
    The purchase date of the transaction associated with the original transaction identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/originalpurchasedate
    """

    expiresDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, an auto-renewable subscription expires or renews.
    
    https://developer.apple.com/documentation/appstoreserverapi/expiresdate
    """

    quantity: Optional[int] = attr.ib(default=None)
    """
    The number of consumable products purchased.
    
    https://developer.apple.com/documentation/appstoreserverapi/quantity
    """

    type: Optional[Type] = Type.create_main_attr('rawType')
    """
    The type of the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/type
    """

    rawType: Optional[str] = Type.create_raw_attr('type')
    """
    See type
    """

    appAccountToken: Optional[str] = attr.ib(default=None)
    """
    The UUID that an app optionally generates to map a customer's in-app purchase with its resulting App Store transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """

    inAppOwnershipType: Optional[InAppOwnershipType] = InAppOwnershipType.create_main_attr('rawInAppOwnershipType')
    """
    A string that describes whether the transaction was purchased by the user, or is available to them through Family Sharing.
    
    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """

    rawInAppOwnershipType: Optional[str] = InAppOwnershipType.create_raw_attr('inAppOwnershipType')
    """
    See inAppOwnershipType
    """

    signedDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature data.
    
    https://developer.apple.com/documentation/appstoreserverapi/signeddate
    """

    revocationReason: Optional[RevocationReason] = RevocationReason.create_main_attr('rawRevocationReason')
    """
    The reason that the App Store refunded the transaction or revoked it from family sharing.
    
    https://developer.apple.com/documentation/appstoreserverapi/revocationreason
    """

    rawRevocationReason: Optional[int] = RevocationReason.create_raw_attr('revocationReason')
    """
    See revocationReason
    """

    revocationDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that Apple Support refunded a transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/revocationdate
    """    

    isUpgraded: Optional[bool] = attr.ib(default=None)
    """
    The Boolean value that indicates whether the user upgraded to another subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/isupgraded
    """

    offerType: Optional[OfferType] = OfferType.create_main_attr('rawOfferType')
    """
    A value that represents the promotional offer type.
    
    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """

    rawOfferType: Optional[int] = OfferType.create_raw_attr('offerType')
    """
    See offerType
    """

    offerIdentifier: Optional[str] = attr.ib(default=None)
    """
    The identifier that contains the promo code or the promotional offer identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/offeridentifier
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment')
    """
    The server environment, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    storefront: Optional[str] = attr.ib(default=None)
    """
    The three-letter code that represents the country or region associated with the App Store storefront for the purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefront
    """

    storefrontId: Optional[str] = attr.ib(default=None)
    """
    An Apple-defined value that uniquely identifies the App Store storefront associated with the purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefrontid
    """

    transactionReason: Optional[TransactionReason] = TransactionReason.create_main_attr('rawTransactionReason')
    """
    The reason for the purchase transaction, which indicates whether it's a customer's purchase or a renewal for an auto-renewable subscription that the system initiates.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionreason
    """

    rawTransactionReason: Optional[str] = TransactionReason.create_raw_attr('transactionReason')
    """
    See transactionReason
    """

    currency: Optional[str] = attr.ib(default=None)
    """
    The three-letter ISO 4217 currency code for the price of the product.
    
    https://developer.apple.com/documentation/appstoreserverapi/currency
    """

    price: Optional[int] = attr.ib(default=None)
    """
    The price, in milliunits, of the in-app purchase or subscription offer that you configured in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/price
    """

    offerDiscountType: Optional[OfferDiscountType] = OfferDiscountType.create_main_attr('rawOfferDiscountType')
    """
    The payment mode you configure for an introductory offer, promotional offer, or offer code on an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/offerdiscounttype
    """

    rawOfferDiscountType: Optional[str] = OfferDiscountType.create_raw_attr('offerDiscountType')
    """
    See offerDiscountType
    """