# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

@define
class AdvancedCommerceRequestInfo:
    """
    The metadata to include in server requests.
    
    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    requestReferenceId: UUID = attr.ib()
    """
    A UUID that you provide to uniquely identify each request. If the request times out, you can use the same requestReferenceId value to retry the request. Otherwise, provide a unique value.
    """

    appAccountToken: Optional[UUID] = attr.ib(default=None)
    """
    A UUID that represents an app account token, to associate with the transaction in the request.
    """

    consistencyToken: Optional[str] = attr.ib(default=None)
    """
    The value of the advancedCommerceConsistencyToken that you receive in the JWSRenewalInfo renewal information for a subscription. Don’t generate this value.
    
    https://developer.apple.com/documentation/AppStoreServerAPI/advancedCommerceConsistencyToken
    """