# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List
from uuid import UUID

from attr import define
import attr

from .AdvancedCommerceRenewalInfo import AdvancedCommerceRenewalInfo
from .AutoRenewStatus import AutoRenewStatus
from .Environment import Environment
from .ExpirationIntent import ExpirationIntent
from .LibraryUtility import AttrsRawValueAware
from .OfferDiscountType import OfferDiscountType
from .OfferType import OfferType
from .PriceIncreaseStatus import PriceIncreaseStatus
from .RenewalBillingPlanType import RenewalBillingPlanType
from .RenewalCommitmentInfo import RenewalCommitmentInfo

@define
class JWSRenewalInfoDecodedPayload(AttrsRawValueAware):
    """
    A decoded payload containing subscription renewal information for an auto-renewable subscription.

    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfodecodedpayload
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

    autoRenewProductId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The identifier of the product that renews at the next billing period.

    https://developer.apple.com/documentation/appstoreserverapi/autorenewproductid
    """

    autoRenewStatus: Optional[AutoRenewStatus] = AutoRenewStatus.create_main_attr('rawAutoRenewStatus', kw_only=True)
    """
    The renewal status of the auto-renewable subscription.

    https://developer.apple.com/documentation/appstoreserverapi/autorenewstatus
    """

    rawAutoRenewStatus: Optional[int] = AutoRenewStatus.create_raw_attr('autoRenewStatus')
    """
    See autoRenewStatus
    """

    currency: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The currency code for the renewalPrice of the subscription.

    https://developer.apple.com/documentation/appstoreserverapi/currency
    """

    eligibleWinBackOfferIds: Optional[List[str]] = attr.ib(default=None, kw_only=True)
    """
    The list of win-back offer IDs that the customer is eligible for.

    https://developer.apple.com/documentation/appstoreserverapi/eligiblewinbackofferids
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

    expirationIntent: Optional[ExpirationIntent] = ExpirationIntent.create_main_attr('rawExpirationIntent', kw_only=True)
    """
    The reason the subscription expired.

    https://developer.apple.com/documentation/appstoreserverapi/expirationintent
    """

    rawExpirationIntent: Optional[int] = ExpirationIntent.create_raw_attr('expirationIntent')
    """
    See expirationIntent
    """

    gracePeriodExpiresDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The time when the Billing Grace Period for subscription renewals expires.

    https://developer.apple.com/documentation/appstoreserverapi/graceperiodexpiresdate
    """

    isInBillingRetryPeriod: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the App Store is attempting to automatically renew the expired subscription.

    https://developer.apple.com/documentation/appstoreserverapi/isinbillingretryperiod
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
    The offer code or the promotional offer identifier.

    https://developer.apple.com/documentation/appstoreserverapi/offeridentifier
    """

    offerPeriod: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The duration of the offer.

    https://developer.apple.com/documentation/appstoreserverapi/offerperiod
    """

    offerType: Optional[OfferType] = OfferType.create_main_attr('rawOfferType', kw_only=True)
    """
    The type of subscription offer.

    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """

    rawOfferType: Optional[int] = OfferType.create_raw_attr('offerType')
    """
    See offerType
    """

    originalTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The transaction identifier of the original purchase associated with this transaction.

    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    priceIncreaseStatus: Optional[PriceIncreaseStatus] = PriceIncreaseStatus.create_main_attr('rawPriceIncreaseStatus', kw_only=True)
    """
    The status that indicates whether the auto-renewable subscription is subject to a price increase.

    https://developer.apple.com/documentation/appstoreserverapi/priceincreasestatus
    """

    rawPriceIncreaseStatus: Optional[int] = PriceIncreaseStatus.create_raw_attr('priceIncreaseStatus')
    """
    See priceIncreaseStatus
    """

    productId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The product identifier of the In-App Purchase.

    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    recentSubscriptionStartDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The earliest start date of the auto-renewable subscription in a series of subscription purchases that ignores all lapses of paid service that are 60 days or fewer.

    https://developer.apple.com/documentation/appstoreserverapi/recentsubscriptionstartdate
    """

    renewalDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, when the most recent auto-renewable subscription purchase expires.

    https://developer.apple.com/documentation/appstoreserverapi/renewaldate
    """

    renewalPrice: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The renewal price, in milliunits, of the auto-renewable subscription that renews at the next billing period.

    https://developer.apple.com/documentation/appstoreserverapi/renewalprice
    """

    signedDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature (JWS) data.

    https://developer.apple.com/documentation/appstoreserverapi/signeddate
    """

    advancedCommerceInfo: Optional[AdvancedCommerceRenewalInfo] = attr.ib(default=None, kw_only=True)
    """
    Renewal information that is present only for Advanced Commerce SKUs.

    https://developer.apple.com/documentation/appstoreserverapi/advancedcommercerenewalinfo
    """

    commitmentInfo: Optional[RenewalCommitmentInfo] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/renewalcommitmentinfo
    """

    renewalBillingPlanType: Optional[RenewalBillingPlanType] = RenewalBillingPlanType.create_main_attr('rawRenewalBillingPlanType', kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/renewalbillingplantype
    """

    rawRenewalBillingPlanType: Optional[str] = RenewalBillingPlanType.create_raw_attr('renewalBillingPlanType')
    """
    See renewalBillingPlanType
    """
