# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

class AutoRenewStatus(Enum): 
    """
    The renewal status for an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/autorenewstatus
    """
    OFF = 0
    ON = 1
