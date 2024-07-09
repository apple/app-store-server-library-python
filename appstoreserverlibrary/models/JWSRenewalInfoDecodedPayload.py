# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import List, Optional

from attr import define
import attr
from .AutoRenewStatus import AutoRenewStatus
from .Environment import Environment

from .ExpirationIntent import ExpirationIntent
from .LibraryUtility import AttrsRawValueAware
from .OfferType import OfferType
from .PriceIncreaseStatus import PriceIncreaseStatus
from .OfferDiscountType import OfferDiscountType

@define
class JWSRenewalInfoDecodedPayload(AttrsRawValueAware):
    """
    A decoded payload containing subscription renewal information for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfodecodedpayload
    """

    expirationIntent: Optional[ExpirationIntent] = ExpirationIntent.create_main_attr('rawExpirationIntent')
    """
    The reason the subscription expired.
    
    https://developer.apple.com/documentation/appstoreserverapi/expirationintent
    """

    rawExpirationIntent: Optional[int] = ExpirationIntent.create_raw_attr('expirationIntent')
    """
    See expirationIntent
    """

    originalTransactionId: Optional[str] = attr.ib(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    autoRenewProductId: Optional[str] = attr.ib(default=None)
    """
    The product identifier of the product that will renew at the next billing period.
    
    https://developer.apple.com/documentation/appstoreserverapi/autorenewproductid
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    autoRenewStatus: Optional[AutoRenewStatus] = AutoRenewStatus.create_main_attr('rawAutoRenewStatus')
    """
    The renewal status of the auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/autorenewstatus
    """

    rawAutoRenewStatus: Optional[int] = AutoRenewStatus.create_raw_attr('autoRenewStatus')
    """
    See autoRenewStatus
    """

    isInBillingRetryPeriod: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether the App Store is attempting to automatically renew an expired subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/isinbillingretryperiod
    """

    priceIncreaseStatus: Optional[PriceIncreaseStatus] = PriceIncreaseStatus.create_main_attr('rawPriceIncreaseStatus')
    """
    The status that indicates whether the auto-renewable subscription is subject to a price increase.
    
    https://developer.apple.com/documentation/appstoreserverapi/priceincreasestatus
    """

    rawPriceIncreaseStatus: Optional[int] = PriceIncreaseStatus.create_raw_attr('priceIncreaseStatus')
    """
    See priceIncreaseStatus
    """

    gracePeriodExpiresDate: Optional[int] = attr.ib(default=None)
    """
    The time when the billing grace period for subscription renewals expires.
    
    https://developer.apple.com/documentation/appstoreserverapi/graceperiodexpiresdate
    """

    offerType: Optional[OfferType] = OfferType.create_main_attr('rawOfferType')
    """
    The type of the subscription offer.
    
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

    signedDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature data.
    
    https://developer.apple.com/documentation/appstoreserverapi/signeddate
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

    recentSubscriptionStartDate: Optional[int] = attr.ib(default=None)
    """
    The earliest start date of a subscription in a series of auto-renewable subscription purchases that ignores all lapses of paid service shorter than 60 days.
    
    https://developer.apple.com/documentation/appstoreserverapi/recentsubscriptionstartdate
    """

    renewalDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the most recent auto-renewable subscription purchase expires.
    
    https://developer.apple.com/documentation/appstoreserverapi/renewaldate
    """

    currency: Optional[str] = attr.ib(default=None)
    """
    The currency code for the renewalPrice of the subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/currency
    """

    renewalPrice: Optional[int] = attr.ib(default=None)
    """
    The renewal price, in milliunits, of the auto-renewable subscription that renews at the next billing period.
    
    https://developer.apple.com/documentation/appstoreserverapi/renewalprice
    """

    offerDiscountType: Optional[OfferDiscountType] = OfferDiscountType.create_main_attr('rawOfferDiscountType')
    """
    The payment mode of the discount offer.
    
    https://developer.apple.com/documentation/appstoreserverapi/offerdiscounttype
    """

    rawOfferDiscountType: Optional[str] = OfferDiscountType.create_raw_attr('offerDiscountType')
    """
    See offerDiscountType
    """

    eligibleWinBackOfferIds: Optional[List[str]] = attr.ib(default=None)
    """
    An array of win-back offer identifiers that a customer is eligible to redeem, which sorts the identifiers to present the better offers first.
    
    https://developer.apple.com/documentation/appstoreserverapi/eligiblewinbackofferids
    """