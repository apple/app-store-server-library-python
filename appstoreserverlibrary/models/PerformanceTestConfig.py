# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .LibraryUtility import validate_not_none

@define
class PerformanceTestConfig:
    """
    An object that enumerates the test configuration parameters.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    maxConcurrentRequests: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The maximum number of concurrent requests the API allows.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    responseTimeThreshold: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The maximum time your server has to respond when the system calls your Get Retention Message endpoint in the sandbox environment.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    successRateThreshold: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The success rate threshold percentage.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    totalDuration: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The total duration of the test in milliseconds.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    totalRequests: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The total number of requests to make during the test.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """
