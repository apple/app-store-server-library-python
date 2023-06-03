# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr
from .Environment import Environment
from .InAppOwnershipType import InAppOwnershipType
from .OfferType import OfferType
from .RevocationReason import RevocationReason
from .TransactionReason import TransactionReason

from .Type import Type

@define
class JWSTransactionDecodedPayload: 
    """
    A decoded payload containing transaction information.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransactiondecodedpayload
    """

    originalTransactionId: str = attr.ib(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    transactionId: str = attr.ib(default=None)
    """
    The unique identifier for a transaction such as an in-app purchase, restored in-app purchase, or subscription renewal.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionid
    """

    webOrderLineItemId: str = attr.ib(default=None)
    """
    The unique identifier of subscription-purchase events across devices, including renewals.
    
    https://developer.apple.com/documentation/appstoreserverapi/weborderlineitemid
    """

    bundleId: str = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    productId: str = attr.ib(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """    

    subscriptionGroupIdentifier: str = attr.ib(default=None)
    """
    The identifier of the subscription group that the subscription belongs to.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifier
    """

    purchaseDate: int = attr.ib(default=None)
    """
    The time that the App Store charged the user's account for an in-app purchase, a restored in-app purchase, a subscription, or a subscription renewal after a lapse.
    
    https://developer.apple.com/documentation/appstoreserverapi/purchasedate
    """

    originalPurchaseDate: int = attr.ib(default=None)
    """
    The purchase date of the transaction associated with the original transaction identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/originalpurchasedate
    """

    expiresDate: int = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, an auto-renewable subscription expires or renews.
    
    https://developer.apple.com/documentation/appstoreserverapi/expiresdate
    """

    quantity: int = attr.ib(default=None)
    """
    The number of consumable products purchased.
    
    https://developer.apple.com/documentation/appstoreserverapi/quantity
    """

    type: Type = attr.ib(default=None)
    """
    The type of the in-app purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/type
    """

    appAccountToken: str = attr.ib(default=None)
    """
    The UUID that an app optionally generates to map a customer's in-app purchase with its resulting App Store transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """

    inAppOwnershipType: InAppOwnershipType = attr.ib(default=None)
    """
    A string that describes whether the transaction was purchased by the user, or is available to them through Family Sharing.
    
    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """

    signedDate: int = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature data.
    
    https://developer.apple.com/documentation/appstoreserverapi/signeddate
    """

    revocationReason: RevocationReason = attr.ib(default=None)
    """
    The reason that the App Store refunded the transaction or revoked it from family sharing.
    
    https://developer.apple.com/documentation/appstoreserverapi/revocationreason
    """

    revocationDate: int = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that Apple Support refunded a transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/revocationdate
    """    

    isUpgraded: bool = attr.ib(default=None)
    """
    The Boolean value that indicates whether the user upgraded to another subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/isupgraded
    """

    offerType: OfferType = attr.ib(default=None)
    """
    A value that represents the promotional offer type.
    
    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """

    offerIdentifier: str = attr.ib(default=None)
    """
    The identifier that contains the promo code or the promotional offer identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/offeridentifier
    """

    environment: Environment = attr.ib(default=None)
    """
    The server environment, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    storefront: str = attr.ib(default=None)
    """
    The three-letter code that represents the country or region associated with the App Store storefront for the purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefront
    """

    storefrontId: str = attr.ib(default=None)
    """
    An Apple-defined value that uniquely identifies the App Store storefront associated with the purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefrontid
    """

    transactionReason: TransactionReason = attr.ib(default=None)
    """
    The reason for the purchase transaction, which indicates whether it's a customer's purchase or a renewal for an auto-renewable subscription that the system initates.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionreason
    """