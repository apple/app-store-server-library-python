# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum


class Type(Enum):
    """
    The type of in-app purchase products you can offer in your app.
    
    https://developer.apple.com/documentation/appstoreserverapi/type
    """
    AUTO_RENEWABLE_SUBSCRIPTION = "Auto-Renewable Subscription"
    NON_CONSUMABLE = "Non-Consumable"
    CONSUMABLE = "Consumable"
    NON_RENEWING_SUBSCRIPTION = "Non-Renewing Subscription"
