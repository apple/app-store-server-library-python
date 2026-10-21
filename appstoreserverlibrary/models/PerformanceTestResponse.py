# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from uuid import UUID

from attr import define
import attr

from .LibraryUtility import validate_not_none
from .PerformanceTestConfig import PerformanceTestConfig

@define
class PerformanceTestResponse:
    """
    The performance test response object.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponse
    """

    config: PerformanceTestConfig = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The performance test configuration object.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    requestId: UUID = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The performance test request identifier.

    https://developer.apple.com/documentation/retentionmessaging/requestid
    """
