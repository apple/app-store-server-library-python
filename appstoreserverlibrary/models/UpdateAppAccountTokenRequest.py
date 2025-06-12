# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
from attr import define
import attr

@define
class UpdateAppAccountTokenRequest:
    """
    The request body that contains an app account token value.

    https://developer.apple.com/documentation/appstoreserverapi/updateappaccounttokenrequest
    """

    appAccountToken: str = attr.ib()
    """
    The UUID that an app optionally generates to map a customer's in-app purchase with its resulting App Store transaction.

    https://developer.apple.com/documentation/appstoreserverapi/appaccounttoken
    """
