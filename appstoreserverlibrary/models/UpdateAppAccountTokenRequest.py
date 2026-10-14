# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class UpdateAppAccountTokenRequest:
    """
    The request body that contains an app account token value.

    https://developer.apple.com/documentation/appstoreserverapi/updateappaccounttokenrequest
    """

    appAccountToken: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A UUID value to associate with the transaction you indicate in the endpoint parameter.

    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """
