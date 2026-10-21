# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware
from .Status import Status

@define
class LastTransactionsItem(AttrsRawValueAware):
    """
    The most recent App Store-signed transaction information and App Store-signed renewal information for an auto-renewable subscription.

    https://developer.apple.com/documentation/appstoreserverapi/lasttransactionsitem
    """

    originalTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The original transaction identifier of the auto-renewable subscription.

    https://developer.apple.com/documentation/appstoreserverapi/originaltransactionid
    """

    status: Optional[Status] = Status.create_main_attr('rawStatus', kw_only=True)
    """
    The status of the auto-renewable subscription.

    https://developer.apple.com/documentation/appstoreserverapi/status
    """

    rawStatus: Optional[int] = Status.create_raw_attr('status')
    """
    See status
    """

    signedRenewalInfo: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The subscription renewal information signed by the App Store, in JSON Web Signature (JWS) format.

    https://developer.apple.com/documentation/appstoreserverapi/jwsrenewalinfo
    """

    signedTransactionInfo: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The transaction information signed by the App Store, in JWS format.

    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """
