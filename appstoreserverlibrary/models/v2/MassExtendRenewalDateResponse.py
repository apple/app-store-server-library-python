# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from pydantic import Field

from appstoreserverlibrary.models.v2.Base import Model


class MassExtendRenewalDateResponse(Model):
    """
    A response that indicates the server successfully received the subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldateresponse
    """

    requestIdentifier: Optional[str] = Field(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """
