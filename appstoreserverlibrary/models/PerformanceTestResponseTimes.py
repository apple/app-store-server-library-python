# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

@define
class PerformanceTestResponseTimes:
    """
    An object that describes test response times.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    average: Optional[int] = attr.ib(default=None)
    """
    Average response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/average
    """

    p50: Optional[int] = attr.ib(default=None)
    """
    The 50th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/p50
    """

    p90: Optional[int] = attr.ib(default=None)
    """
    The 90th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/p90
    """

    p95: Optional[int] = attr.ib(default=None)
    """
    The 95th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/p95
    """

    p99: Optional[int] = attr.ib(default=None)
    """
    The 99th percentile response time in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/p99
    """
