# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class PerformanceTestStatus(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The status of the performance test.

    https://developer.apple.com/documentation/retentionmessaging/performanceteststatus
    """
    PENDING = "PENDING"
    PASS = "PASS"
    FAIL = "FAIL"
