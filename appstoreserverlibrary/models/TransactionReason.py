# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

class TransactionReason(Enum): 
    """
    The cause of a purchase transaction, which indicates whether it’s a customer’s purchase or a renewal for an auto-renewable subscription that the system initiates.
    
    https://developer.apple.com/documentation/appstoreserverapi/transactionreason
    """
    PURCHASE = "PURCHASE"
    RENEWAL = "RENEWAL"
