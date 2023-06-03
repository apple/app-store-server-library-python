# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .Environment import Environment

@define
class HistoryResponse: 
    """
    A response that contains the customer's transaction history for an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/historyresponse
    """

    revision: str = attr.ib(default=None)
    """
    A token you use in a query to request the next set of transactions for the customer.
    
    https://developer.apple.com/documentation/appstoreserverapi/revision
    """

    hasMore: bool = attr.ib(default=None)
    """
    A Boolean value indicating whether the App Store has more transaction data.
    
    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """

    bundleId: str = attr.ib(default=None)
    """
    The bundle identifier of an app.
    
    https://developer.apple.com/documentation/appstoreserverapi/bundleid
    """

    appAppleId: int = attr.ib(default=None)
    """
    The unique identifier of an app in the App Store.
    
    https://developer.apple.com/documentation/appstoreservernotifications/appappleid
    """

    environment: Environment = attr.ib(default=None)
    """
    The server environment in which you're making the request, whether sandbox or production.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """

    signedTransactions: "list[str]" = attr.ib(default=None)
    """
    An array of in-app purchase transactions for the customer, signed by Apple, in JSON Web Signature format.
    
    https://developer.apple.com/documentation/appstoreserverapi/jwstransaction
    """