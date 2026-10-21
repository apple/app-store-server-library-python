# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .ConsumptionRequestReason import ConsumptionRequestReason
from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware
from .Status import Status

@define
class Data(AttrsRawValueAware):
    """
    The payload data that contains app metadata and the signed renewal and transaction information.

    https://developer.apple.com/documentation/appstoreservernotifications/data
    """

    appAppleId: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the app that the notification applies to.

    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The bundle identifier of the app.

    https://developer.apple.com/documentation/appstoreservernotifications/bundleid
    """

    bundleVersion: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The version of the build that identifies an iteration of the bundle.

    https://developer.apple.com/documentation/appstoreservernotifications/bundleversion
    """

    consumptionRequestReason: Optional[ConsumptionRequestReason] = ConsumptionRequestReason.create_main_attr('rawConsumptionRequestReason', kw_only=True)
    """
    The reason the customer requested the refund.

    https://developer.apple.com/documentation/appstoreservernotifications/consumptionrequestreason
    """

    rawConsumptionRequestReason: Optional[str] = ConsumptionRequestReason.create_raw_attr('consumptionRequestReason')
    """
    See consumptionRequestReason
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment', kw_only=True)
    """
    The server environment that the notification applies to, either sandbox or production.

    https://developer.apple.com/documentation/appstoreservernotifications/environment
    """

    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    signedRenewalInfo: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    Subscription renewal information signed by the App Store, in JSON Web Signature (JWS) format.

    https://developer.apple.com/documentation/appstoreservernotifications/jwsrenewalinfo
    """

    signedTransactionInfo: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    Transaction information signed by the App Store, in JSON Web Signature (JWS) format.

    https://developer.apple.com/documentation/appstoreservernotifications/jwstransaction
    """

    status: Optional[Status] = Status.create_main_attr('rawStatus', kw_only=True)
    """
    The status of an auto-renewable subscription as of the signedDate in the responseBodyV2DecodedPayload.

    https://developer.apple.com/documentation/appstoreservernotifications/status
    """

    rawStatus: Optional[int] = Status.create_raw_attr('status')
    """
    See status
    """
