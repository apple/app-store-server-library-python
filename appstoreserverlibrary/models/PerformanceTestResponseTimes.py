# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class PerformanceTestResponseTimes:
    """
    An object that describes test response times.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    average: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    Average response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    p50: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The 50th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    p90: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The 90th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    p95: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The 95th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    p99: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The 99th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """
