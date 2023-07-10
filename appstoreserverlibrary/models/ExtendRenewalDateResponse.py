# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

@define
class ExtendRenewalDateResponse: 
    """
    A response that indicates whether an individual renewal-date extension succeeded, and related details.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendrenewaldateresponse
    """

    originalTransactionId: Optional[str] = attr.ib(default=None)
    """
    The original transaction identifier of a purchase.
    
    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    webOrderLineItemId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier of subscription-purchase events across devices, including renewals.
    
    https://developer.apple.com/documentation/appstoreserverapi/weborderlineitemid
    """

    success: Optional[bool] = attr.ib(default=None)
    """
    A Boolean value that indicates whether the subscription-renewal-date extension succeeded.
    
    https://developer.apple.com/documentation/appstoreserverapi/success
    """

    effectiveDate: Optional[int] = attr.ib(default=None)
    """
    The new subscription expiration date for a subscription-renewal extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/effectivedate
    """