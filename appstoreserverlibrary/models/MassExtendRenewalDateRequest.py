# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
from typing import List, Optional
import attr

from .ExtendReasonCode import ExtendReasonCode

@define
class MassExtendRenewalDateRequest: 
    """
    The request body that contains subscription-renewal-extension data to apply for all eligible active subscribers.
    
    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldaterequest
    """

    extendByDays: Optional[int] = attr.ib(default=None)
    """
    The number of days to extend the subscription renewal date.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendbydays
    maximum: 90
    """

    extendReasonCode: Optional[ExtendReasonCode] = attr.ib(default=None)
    """
    The reason code for the subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """    

    requestIdentifier: Optional[str] = attr.ib(default=None)
    """
    A string that contains a unique identifier you provide to track each subscription-renewal-date extension request.
    
    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    storefrontCountryCodes: Optional[List[str]] = attr.ib(default=None)
    """
    A list of storefront country codes you provide to limit the storefronts for a subscription-renewal-date extension.
    
    https://developer.apple.com/documentation/appstoreserverapi/storefrontcountrycodes
    """

    productId: Optional[str] = attr.ib(default=None)
    """
    The unique identifier for the product, that you create in App Store Connect.
    
    https://developer.apple.com/documentation/appstoreserverapi/productid
    """