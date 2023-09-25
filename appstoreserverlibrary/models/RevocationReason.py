# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import IntEnum

class RevocationReason(IntEnum): 
    """
    The reason for a refunded transaction.
    
    https://developer.apple.com/documentation/appstoreserverapi/revocationreason
    """
    REFUNDED_DUE_TO_ISSUE = 1
    REFUNDED_FOR_OTHER_REASON = 0
