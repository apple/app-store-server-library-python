# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Dict, Optional

from attr import define, Attribute
import attr

from .LibraryUtility import AttrsRawValueAware, metadata_key, metadata_type_key
from .PerformanceTestConfig import PerformanceTestConfig
from .PerformanceTestResponseTimes import PerformanceTestResponseTimes
from .PerformanceTestStatus import PerformanceTestStatus
from .SendAttemptResult import SendAttemptResult

def _failures_value_set(self, _: Attribute, value: Optional[Dict[SendAttemptResult, int]]):
    new_raw = {k.value: v for k, v in value.items()} if value is not None else None
    if new_raw != getattr(self, 'rawFailures'):
        object.__setattr__(self, 'rawFailures', new_raw)
    return value

def _raw_failures_value_set(self, _: Attribute, value: Optional[Dict[str, int]]):
    new_typed = {}
    if value is not None:
        for k, v in value.items():
            if k in SendAttemptResult:
                new_typed[SendAttemptResult(k)] = v
    new_typed = new_typed if new_typed else None
    if new_typed != getattr(self, 'failures'):
        object.__setattr__(self, 'failures', new_typed)
    return value

@define
class PerformanceTestResultResponse(AttrsRawValueAware):
    """
    An object the API returns that describes the performance test results.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresultresponse
    """

    config: Optional[PerformanceTestConfig] = attr.ib(default=None)
    """
    A PerformanceTestConfig object that enumerates the test parameters.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    target: Optional[str] = attr.ib(default=None)
    """
    The target URL for the performance test.

    https://developer.apple.com/documentation/retentionmessaging/target
    """

    result: Optional[PerformanceTestStatus] = PerformanceTestStatus.create_main_attr('rawResult')
    """
    A PerformanceTestStatus object that describes the overall result of the test.

    https://developer.apple.com/documentation/retentionmessaging/performanceteststatus
    """

    rawResult: Optional[str] = PerformanceTestStatus.create_raw_attr('result')
    """
    See result
    """

    successRate: Optional[int] = attr.ib(default=None)
    """
    An integer that describes he success rate percentage of the performance test.

    https://developer.apple.com/documentation/retentionmessaging/successrate
    """

    numPending: Optional[int] = attr.ib(default=None)
    """
    An integer that describes the number of pending requests in the performance test.

    https://developer.apple.com/documentation/retentionmessaging/numpending
    """

    responseTimes: Optional[PerformanceTestResponseTimes] = attr.ib(default=None)
    """
    A PerformanceTestResponseTimes object that enumerates the response times measured during the test.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    failures: Optional[Dict[SendAttemptResult, int]] = attr.ib(default=None, on_setattr=_failures_value_set, metadata={metadata_key: 'rawFailures', metadata_type_key: 'main'})
    """
    A map of server-to-server notification failure reasons and counts that represent the number of failures encountered during the performance test.

    https://developer.apple.com/documentation/retentionmessaging/failures
    """

    rawFailures: Optional[Dict[str, int]] = attr.ib(default=None, kw_only=True, on_setattr=_raw_failures_value_set, metadata={metadata_key: 'failures', metadata_type_key: 'raw'})
    """
    See failures
    """
