# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

@define
class MassExtendRenewalDateResponse: 
    """
    A response that indicates the server successfully received the subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldateresponse
    """

    requestIdentifier: Optional[str] = attr.ib(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """