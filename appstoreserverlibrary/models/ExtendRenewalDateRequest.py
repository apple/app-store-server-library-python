# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .ExtendReasonCode import ExtendReasonCode

@define
class ExtendRenewalDateRequest: 
    """
    The request body that contains subscription-renewal-extension data for an individual subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendrenewaldaterequest
    """

    extendByDays: Optional[int] = attr.ib(default=None)
    """
    The number of days to extend the subscription renewal date.

    https://developer.apple.com/documentation/appstoreserverapi/extendbydays
    maximum: 90
    """

    extendReasonCode: Optional[ExtendReasonCode] = attr.ib(default=None)
    """
    The reason code for the subscription date extension
    
    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """

    requestIdentifier: Optional[str] = attr.ib(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """