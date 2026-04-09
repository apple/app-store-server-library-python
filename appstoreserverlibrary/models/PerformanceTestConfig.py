# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

@define
class PerformanceTestConfig:
    """
    An object that enumerates the test configuration parameters.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    maxConcurrentRequests: Optional[int] = attr.ib(default=None)
    """
    The maximum number of concurrent requests the API allows.

    https://developer.apple.com/documentation/retentionmessaging/maxconcurrentrequests
    """

    totalRequests: Optional[int] = attr.ib(default=None)
    """
    The total number of requests to make during the test.

    https://developer.apple.com/documentation/retentionmessaging/totalrequests
    """

    totalDuration: Optional[int] = attr.ib(default=None)
    """
    The total duration of the test in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/totalduration
    """

    responseTimeThreshold: Optional[int] = attr.ib(default=None)
    """
    The maximum time your server has to respond when the system calls your Get Retention Message endpoint in the sandbox environment.

    https://developer.apple.com/documentation/retentionmessaging/responsetimethreshold
    """

    successRateThreshold: Optional[int] = attr.ib(default=None)
    """
    The success rate threshold percentage.

    https://developer.apple.com/documentation/retentionmessaging/successratethreshold
    """
