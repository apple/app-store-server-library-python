# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .AdvancedCommerceTransactionInfo import AdvancedCommerceTransactionInfo
from .BillingPlanType import BillingPlanType
from .Environment import Environment
from .InAppOwnershipType import InAppOwnershipType
from .LibraryUtility import AttrsRawValueAware
from .OfferDiscountType import OfferDiscountType
from .OfferType import OfferType
from .RevocationReason import RevocationReason
from .RevocationType import RevocationType
from .TransactionCommitmentInfo import TransactionCommitmentInfo
from .TransactionReason import TransactionReason
from .Type import Type

@define
class JWSTransactionDecodedPayload(AttrsRawValueAware):
    """
    A decoded payload that contains transaction information.

    https://developer.apple.com/documentation/appstoreserverapi/jwstransactiondecodedpayload
    """

    appAccountToken: Optional[UUID] = attr.ib(default=None, kw_only=True)
    """
    A UUID you create at the time of purchase that associates the transaction with a customer on your own service.

    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """

    appTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the app download transaction.

    https://developer.apple.com/documentation/appstoreserverapi/apptransactionid
    """

    bundleId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The bundle identifier of the app.

    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    currency: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The three-letter ISO 4217 currency code associated with the price parameter.

    https://developer.apple.com/documentation/appstoreserverapi/currency
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment', kw_only=True)
    """
    The server environment, either sandbox or production.

    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    expiresDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that the subscription expires or renews.

    https://developer.apple.com/documentation/appstoreserverapi/expiresdate
    """

    inAppOwnershipType: Optional[InAppOwnershipType] = InAppOwnershipType.create_main_attr('rawInAppOwnershipType', kw_only=True)
    """
    A string that describes whether the transaction was purchased by the customer, or is available to them through Family Sharing, an organization, or a group.

    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """

    rawInAppOwnershipType: Optional[str] = InAppOwnershipType.create_raw_attr('inAppOwnershipType')
    """
    See inAppOwnershipType
    """

    isUpgraded: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the customer upgraded to another subscription.

    https://developer.apple.com/documentation/appstoreserverapi/isupgraded
    """

    offerDiscountType: Optional[OfferDiscountType] = OfferDiscountType.create_main_attr('rawOfferDiscountType', kw_only=True)
    """
    The payment mode you configure for the offer.

    https://developer.apple.com/documentation/appstoreserverapi/offerdiscounttype
    """

    rawOfferDiscountType: Optional[str] = OfferDiscountType.create_raw_attr('offerDiscountType')
    """
    See offerDiscountType
    """

    offerIdentifier: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The identifier that contains the offer code or the promotional offer identifier.

    https://developer.apple.com/documentation/appstoreserverapi/offeridentifier
    """

    offerPeriod: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The duration of the offer applied to the transaction.

    https://developer.apple.com/documentation/appstoreserverapi/offerperiod
    """

    offerType: Optional[OfferType] = OfferType.create_main_attr('rawOfferType', kw_only=True)
    """
    A value that represents the promotional offer type.

    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """

    rawOfferType: Optional[int] = OfferType.create_raw_attr('offerType')
    """
    See offerType
    """

    originalPurchaseDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that represents the purchase date of the original transaction identifier.

    https://developer.apple.com/documentation/appstoreserverapi/originalpurchasedate
    """

    originalTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The transaction identifier of the original purchase.

    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    price: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    An integer value that represents the price multiplied by 1000 of the in-app purchase or subscription offer you configured in App Store Connect and that the system records at the time of the purchase.

    https://developer.apple.com/documentation/appstoreserverapi/price
    """

    productId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the product.

    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    purchaseDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that the App Store charged the customer’s account for a purchase, restored product, subscription, or subscription renewal after a lapse.

    https://developer.apple.com/documentation/appstoreserverapi/purchasedate
    """

    quantity: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The number of products or seats the customer purchased.

    https://developer.apple.com/documentation/appstoreserverapi/quantity
    """

    revocationDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that the App Store refunded the transaction or revoked it from Family Sharing.

    https://developer.apple.com/documentation/appstoreserverapi/revocationdate
    """

    revocationPercentage: Optional[int] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.and_(attr.validators.ge(0), attr.validators.le(100000))))
    """
    The percentage, in milliunits, of the transaction that the App Store has refunded or revoked.

    https://developer.apple.com/documentation/appstoreserverapi/revocationpercentage
    """

    revocationReason: Optional[RevocationReason] = RevocationReason.create_main_attr('rawRevocationReason', kw_only=True)
    """
    The reason that the App Store refunded the transaction or revoked it from Family Sharing.

    https://developer.apple.com/documentation/appstoreserverapi/revocationreason
    """

    rawRevocationReason: Optional[int] = RevocationReason.create_raw_attr('revocationReason')
    """
    See revocationReason
    """

    revocationType: Optional[RevocationType] = RevocationType.create_main_attr('rawRevocationType', kw_only=True)
    """
    The type of the refund or revocation that applies to the transaction.

    https://developer.apple.com/documentation/appstoreserverapi/revocationtype
    """

    rawRevocationType: Optional[str] = RevocationType.create_raw_attr('revocationType')
    """
    See revocationType
    """

    signedDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature (JWS) data.

    https://developer.apple.com/documentation/appstoreserverapi/signeddate
    """

    storefront: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The three-letter code that represents the country or region associated with the App Store storefront for the purchase.

    https://developer.apple.com/documentation/appstoreserverapi/storefront
    """

    storefrontId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    An Apple-defined value that uniquely identifies the App Store storefront associated with the purchase.

    https://developer.apple.com/documentation/appstoreserverapi/storefrontid
    """

    subscriptionGroupIdentifier: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The identifier of the subscription group to which the subscription belongs.

    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifier
    """

    transactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the transaction.

    https://developer.apple.com/documentation/appstoreserverapi/transactionid
    """

    transactionReason: Optional[TransactionReason] = TransactionReason.create_main_attr('rawTransactionReason', kw_only=True)
    """
    The reason for the purchase transaction, which indicates whether it’s a customer’s purchase or a renewal for an auto-renewable subscription that the system initiates.

    https://developer.apple.com/documentation/appstoreserverapi/transactionreason
    """

    rawTransactionReason: Optional[str] = TransactionReason.create_raw_attr('transactionReason')
    """
    See transactionReason
    """

    type: Optional[Type] = Type.create_main_attr('rawType', kw_only=True)
    """
    The type of the in-app purchase.

    https://developer.apple.com/documentation/appstoreserverapi/type
    """

    rawType: Optional[str] = Type.create_raw_attr('type')
    """
    See type
    """

    webOrderLineItemId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of subscription purchase events across devices, including subscription renewals.

    https://developer.apple.com/documentation/appstoreserverapi/weborderlineitemid
    """

    advancedCommerceInfo: Optional[AdvancedCommerceTransactionInfo] = attr.ib(default=None, kw_only=True)
    """
    Transaction information that is present only for Advanced Commerce SKUs.

    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercetransactioninfo
    """

    billingPlanType: Optional[BillingPlanType] = BillingPlanType.create_main_attr('rawBillingPlanType', kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/billingplantype
    """

    rawBillingPlanType: Optional[str] = BillingPlanType.create_raw_attr('billingPlanType')
    """
    See billingPlanType
    """

    commitmentInfo: Optional[TransactionCommitmentInfo] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/transactioncommitmentinfo
    """

    previousOriginalTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The subscription’s original transaction identifier, before you migrated the subscription.

    https://developer.apple.com/documentation/appstoreservernotifications/previousoriginaltransactionid
    """
