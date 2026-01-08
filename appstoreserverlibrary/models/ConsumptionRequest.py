# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .DeliveryStatus import DeliveryStatus
from .LibraryUtility import AttrsRawValueAware
from .RefundPreference import RefundPreference

@define
class ConsumptionRequest(AttrsRawValueAware):
    """
    The request body that contains consumption information for an In-App Purchase.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionrequest
    """

    customerConsented: bool = attr.ib()
    """
    A Boolean value that indicates whether the customer consented to provide consumption data to the App Store.

    https://developer.apple.com/documentation/appstoreserverapi/customerconsented
    """

    sampleContentProvided: bool = attr.ib()
    """
    A Boolean value that indicates whether you provided, prior to its purchase, a free sample or trial of the content, or information about its functionality.

    https://developer.apple.com/documentation/appstoreserverapi/samplecontentprovided
    """

    deliveryStatus: Optional[DeliveryStatus] = DeliveryStatus.create_main_attr('rawDeliveryStatus', raw_required=True)
    """
    A value that indicates whether the app successfully delivered an in-app purchase that works properly.

    https://developer.apple.com/documentation/appstoreserverapi/deliverystatus
    """
    
    consumptionPercentage: Optional[int] = attr.ib(default=None)
    """
    An integer that indicates the percentage, in milliunits, of the In-App Purchase the customer consumed.

    https://developer.apple.com/documentation/appstoreserverapi/consumptionpercentage
    """

    rawDeliveryStatus: str = DeliveryStatus.create_raw_attr('deliveryStatus', required=True)
    """
    See deliveryStatus
    """

    refundPreference: Optional[RefundPreference] = RefundPreference.create_main_attr('rawRefundPreference')
    """
    A value that indicates your preferred outcome for the refund request.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreference
    """

    rawRefundPreference: Optional[str] = RefundPreference.create_raw_attr('refundPreference')
    """
    See refundPreference
    """
