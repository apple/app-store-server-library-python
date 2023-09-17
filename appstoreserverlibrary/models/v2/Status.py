# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum


class Status(Enum):
    """
    The status of an auto-renewable subscription.
    
    https://developer.apple.com/documentation/appstoreserverapi/status
    """
    ACTIVE = 1
    EXPIRED = 2
    BILLING_RETRY = 3
    BILLING_GRACE_PERIOD = 4
    REVOKED = 5
