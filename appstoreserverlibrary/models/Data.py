# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .ConsumptionRequestReason import ConsumptionRequestReason
from .Environment import Environment
from .Status import Status
from .LibraryUtility import AttrsRawValueAware

@define
class Data(AttrsRawValueAware):
    """
    The app metadata and the signed renewal and transaction information.
    
    https://developer.apple.com/documentation/appstoreservernotifications/data
    """
    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment')
    """
    The server environment that the notification applies to, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreservernotifications/environment
    """
    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    appAppleId: Optional[int] = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    bundleVersion: Optional[str] = attr.ib(default=None)
    """
    The version of the build that identifies an iteration of the bundle.
    
    https://developer.apple.com/documentation/appstoreservernotifications/bundleversion
    """

    signedTransactionInfo: Optional[str] = attr.ib(default=None)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """

    signedRenewalInfo: Optional[str] = attr.ib(default=None)
    """
    Subscription renewal information, signed by the App Store, in JSON Web Signature (JWS) format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo
    """
        
    status: Optional[Status] = Status.create_main_attr('rawStatus')
    """
    The status of an auto-renewable subscription as of the signedDate in the responseBodyV2DecodedPayload.
    
    https://developer.apple.com/documentation/appstoreservernotifications/status
    """

    rawStatus: Optional[int] = Status.create_raw_attr('status')
    """
    See status
    """

    consumptionRequestReason: Optional[ConsumptionRequestReason] = ConsumptionRequestReason.create_main_attr('rawConsumptionRequestReason')
    """
    The reason the customer requested the refund.
    
    https://developer.apple.com/documentation/appstoreservernotifications/consumptionrequestreason
    """

    rawConsumptionRequestReason: Optional[str] = ConsumptionRequestReason.create_raw_attr('consumptionRequestReason')
    """
    See consumptionRequestReason
    """