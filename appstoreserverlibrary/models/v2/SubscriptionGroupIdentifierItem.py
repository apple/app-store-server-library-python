# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional, List

from pydantic import Field

from .Base import Model
from .LastTransactionsItem import LastTransactionsItem


class SubscriptionGroupIdentifierItem(Model):
    """
    Information for auto-renewable subscriptions, including signed transaction information and signed renewal information, for one subscription group.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifieritem
    """

    subscriptionGroupIdentifier: Optional[str] = Field(default=None)
    """
    The identifier of the subscription group that the subscription belongs to.
    
    https://developer.apple.com/documentation/appstoreserverapi/subscriptiongroupidentifier
    """

    lastTransactions: Optional[List[LastTransactionsItem]] = Field(default=None)
    """
    An array of the most recent App Store-signed transaction information and App Store-signed renewal information for all auto-renewable subscriptions in the subscription group.
    """
