# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .PerformanceTestConfig import PerformanceTestConfig

@define
class PerformanceTestResponse:
    """
    The performance test response object.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponse
    """

    config: Optional[PerformanceTestConfig] = attr.ib(default=None)
    """
    The performance test configuration object.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    requestId: Optional[str] = attr.ib(default=None)
    """
    The performance test request identifier.

    https://developer.apple.com/documentation/retentionmessaging/requestid
    """
