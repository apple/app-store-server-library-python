# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

class OfferType(Enum): 
    """
    The type of subscription offer.
    
    https://developer.apple.com/documentation/appstoreserverapi/offertype
    """
    INTRODUCTORY_OFFER = 1
    PROMOTIONAL_OFFER = 2
    SUBSCRIPTION_OFFER_CODE = 3
