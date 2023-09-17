# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from .Base import Model
from .ExtendReasonCode import ExtendReasonCode


class ExtendRenewalDateRequest(Model):
    """
    The request body that contains subscription-renewal-extension data for an individual subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendrenewaldaterequest
    """

    extendByDays: Optional[int] = Field(default=None)
    """
    The number of days to extend the subscription renewal date.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendbydays
    maximum: 90
    """

    extendReasonCode: Optional[ExtendReasonCode] = Field(default=None)
    """
    The reason code for the subscription date extension
    
    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """

    requestIdentifier: Optional[str] = Field(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """
