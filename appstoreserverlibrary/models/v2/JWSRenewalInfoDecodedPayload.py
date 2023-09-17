# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr
from pydantic import Field

from .AutoRenewStatus import AutoRenewStatus
from .Base import Model
from .Environment import Environment

from .ExpirationIntent import ExpirationIntent
from .OfferType import OfferType
from .PriceIncreaseStatus import PriceIncreaseStatus


class JWSRenewalInfoDecodedPayload(Model):
    """
    A decoded payload containing subscription renewal information for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfodecodedpayload
    """

    expirationIntent: Optional[ExpirationIntent] = Field(default=None)
    """
    The reason the subscription expired.
    
    https://developer.apple.com/documentation/appstoreserverapi/expirationintent
    """

    originalTransactionId: Optional[str] = Field(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    autoRenewProductId: Optional[str] = Field(default=None)
    """
    The product identifier of the product that will renew at the next billing period.
    
    https://developer.apple.com/documentation/appstoreserverapi/autorenewproductid
    """

    productId: Optional[str] = Field(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    autoRenewStatus: Optional[AutoRenewStatus] = Field(default=None)
    """
    The renewal status of the auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/autorenewstatus
    """

    isInBillingRetryPeriod: Optional[bool] = Field(default=None)
    """
    A Boolean value that indicates whether the App Store is attempting to automatically renew an expired subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/isinbillingretryperiod
    """

    priceIncreaseStatus: Optional[PriceIncreaseStatus] = Field(default=None)
    """
    The status that indicates whether the auto-renewable subscription is subject to a price increase.
    
    https://developer.apple.com/documentation/appstoreserverapi/priceincreasestatus
    """

    gracePeriodExpiresDate: Optional[int] = Field(default=None)
    """
    The time when the billing grace period for subscription renewals expires.
    
    https://developer.apple.com/documentation/appstoreserverapi/graceperiodexpiresdate
    """

    offerType: Optional[OfferType] = Field(default=None)
    """
    The type of the subscription offer.
    
    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """

    offerIdentifier: Optional[str] = Field(default=None)
    """
    The identifier that contains the promo code or the promotional offer identifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/offeridentifier
    """

    signedDate: Optional[int] = Field(default=None)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature data.
    
    https://developer.apple.com/documentation/appstoreserverapi/signeddate
    """

    environment: Optional[Environment] = Field(default=None)
    """
    The server environment, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    recentSubscriptionStartDate: Optional[int] = Field(default=None)
    """
    The earliest start date of a subscription in a series of auto-renewable subscription purchases that ignores all lapses of paid service shorter than 60 days.
    
    https://developer.apple.com/documentation/appstoreserverapi/recentsubscriptionstartdate
    """

    renewalDate: Optional[int] = Field(default=None)
    """
    The UNIX time, in milliseconds, that the most recent auto-renewable subscription purchase expires.
    
    https://developer.apple.com/documentation/appstoreserverapi/renewaldate
    """
