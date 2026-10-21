# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .Environment import Environment
from .LibraryUtility import AttrsRawValueAware

@define
class HistoryResponse(AttrsRawValueAware):
    """
    A response that contains the customer’s transaction history for an app.

    https://developer.apple.com/documentation/appstoreserverapi/historyresponse
    """

    appAppleId: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The app’s identifier in the App Store.

    https://developer.apple.com/documentation/appstoreserverapi/appappleid
    """

    bundleId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The bundle identifier of the app.

    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    environment: Optional[Environment] = Environment.create_main_attr('rawEnvironment', kw_only=True)
    """
    The server environment in which you’re making the request, whether sandbox or production.

    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    rawEnvironment: Optional[str] = Environment.create_raw_attr('environment')
    """
    See environment
    """

    hasMore: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the App Store has more transactions than it returns in this response.

    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """

    revision: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A token you use in a query to request the next set of transactions from the endpoint.

    https://developer.apple.com/documentation/appstoreserverapi/revision
    """

    signedTransactions: Optional[List[str]] = attr.ib(default=None, kw_only=True)
    """
    An array of in-app purchase transactions for the customer, signed by Apple, in JSON Web Signature (JWS) format.

    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """
