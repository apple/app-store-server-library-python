# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

class InAppOwnershipType(str, Enum): 
    """
    The relationship of the user with the family-shared purchase to which they have access.
    
    https://developer.apple.com/documentation/appstoreserverapi/inappownershiptype
    """
    FAMILY_SHARED = "FAMILY_SHARED"
    PURCHASED = "PURCHASED"
