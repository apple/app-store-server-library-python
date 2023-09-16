# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum
from typing import List, Optional
import attr


from .InAppOwnershipType import InAppOwnershipType

class ProductType(str, Enum):
    AUTO_RENEWABLE = "AUTO_RENEWABLE"
    NON_RENEWABLE = "NON_RENEWABLE"
    CONSUMABLE = "CONSUMABLE"
    NON_CONSUMABLE = "NON_CONSUMABLE"

class Order(str, Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"

@attr.define
class TransactionHistoryRequest:
    startDate: Optional[int] = attr.ib(default=None)
    """
    An optional start date of the timespan for the transaction history records you're requesting. The startDate must precede the endDate if you specify both dates. To be included in results, the transaction's purchaseDate must be equal to or greater than the startDate.
    
    https://developer.apple.com/documentation/appstoreserverapi/startdate
    """
    
    endDate: Optional[int] = attr.ib(default=None)
    """
    An optional end date of the timespan for the transaction history records you're requesting. Choose an endDate that's later than the startDate if you specify both dates. Using an endDate in the future is valid. To be included in results, the transaction's purchaseDate must be less than the endDate.
    
    https://developer.apple.com/documentation/appstoreserverapi/enddate
    """

    productIds: Optional[List[str]] = attr.ib(default=None)
    """
    An optional filter that indicates the product identifier to include in the transaction history. Your query may specify more than one productID.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """    

    productTypes: Optional[List[ProductType]] = attr.ib(default=None)
    """
    An optional filter that indicates the product type to include in the transaction history. Your query may specify more than one productType.
    """
    
    sort: Optional[Order] = attr.ib(default=None)
    """
    An optional sort order for the transaction history records. The response sorts the transaction records by their recently modified date. The default value is ASCENDING, so you receive the oldest records first.
    """

    subscriptionGroupIdentifiers: Optional[List[str]] = attr.ib(default=None)
    """
    An optional filter that indicates the subscription group identifier to include in the transaction history. Your query may specify more than one subscriptionGroupIdentifier.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifier
    """

    inAppOwnershipType: Optional[InAppOwnershipType] = attr.ib(default=None)
    """
    An optional filter that limits the transaction history by the in-app ownership type.
    
    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """
   
    revoked: Optional[bool] = attr.ib(default=None)
    """
    An optional Boolean value that indicates whether the response includes only revoked transactions when the value is true, or contains only nonrevoked transactions when the value is false. By default, the request doesn't include this parameter.
    """
