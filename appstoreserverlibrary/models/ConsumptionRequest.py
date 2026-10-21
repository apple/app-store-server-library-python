# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .DeliveryStatus import DeliveryStatus
from .LibraryUtility import AttrsRawValueAware, validate_not_none
from .RefundPreference import RefundPreference

@define
class ConsumptionRequest(AttrsRawValueAware):
    """
    The request body that contains consumption information for an In-App Purchase.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequest
    """

    customerConsented: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value of true or false that indicates whether the customer consented to provide consumption data.

    https://developer.apple.com/documentation/appstoreserverapi/customerconsented
    """

    deliveryStatus: DeliveryStatus = DeliveryStatus.create_main_attr('rawDeliveryStatus', raw_required=True, kw_only=True)
    """
    A value that indicates whether the app successfully delivered an In-App Purchase that works properly.

    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """

    rawDeliveryStatus: str = DeliveryStatus.create_raw_attr('deliveryStatus', required=True)
    """
    See deliveryStatus
    """

    sampleContentProvided: bool = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A Boolean value of true or false that indicates whether you provided, prior to its purchase, a free sample or trial of the content, or information about its functionality.

    https://developer.apple.com/documentation/appstoreserverapi/samplecontentprovided
    """

    consumptionPercentage: Optional[int] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.and_(attr.validators.ge(0), attr.validators.le(100000))))
    """
    An integer that indicates the percentage of the In-App Purchase the customer consumed, in milliunits.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionpercentage
    """

    refundPreference: Optional[RefundPreference] = RefundPreference.create_main_attr('rawRefundPreference', kw_only=True)
    """
    A value that indicates your preference, based on your operational logic, as to whether the App Store should grant the refund.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreference
    """

    rawRefundPreference: Optional[str] = RefundPreference.create_raw_attr('refundPreference')
    """
    See refundPreference
    """
