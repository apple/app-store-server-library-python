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

    effectiveDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The new subscription expiration date of a successful subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/effectivedate
    """

    originalTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The original transaction identifier of the subscription that experienced a service interruption.

    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    success: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the subscription-renewal-date extension succeeded.

    https://developer.apple.com/documentation/appstoreserverapi/success
    """

    webOrderLineItemId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A unique ID that identifies subscription-purchase events, including subscription renewals, across devices.

    https://developer.apple.com/documentation/appstoreserverapi/weborderlineitemid
    """
