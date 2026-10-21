# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional
from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class AdvancedCommerceRequestInfo:
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    requestReferenceId: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A UUID that you provide to uniquely identify each request.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    appAccountToken: Optional[UUID] = attr.ib(default=None, kw_only=True)
    """
    A UUID that represents an app account token, to associate with the transaction in the request.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """

    consistencyToken: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The value of the advancedCommerceConsistencyToken that you receive in the JWSRenewalInfo renewal information for a subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """
