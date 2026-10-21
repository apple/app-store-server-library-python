# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Dict

from attr import define, Attribute
import attr

from .LibraryUtility import AttrsRawValueAware, metadata_key, metadata_required_key, metadata_type_key, validate_not_none
from .PerformanceTestConfig import PerformanceTestConfig
from .PerformanceTestResponseTimes import PerformanceTestResponseTimes
from .PerformanceTestStatus import PerformanceTestStatus
from .SendAttemptResult import SendAttemptResult

def _failures_value_set(self, attribute: Attribute, value: Dict[SendAttemptResult, int]):
    if value is None:
        raise ValueError(f"{attribute.name} cannot be set to None when field is required")
    new_raw = {k.value: v for k, v in value.items()}
    if new_raw != getattr(self, 'rawFailures'):
        object.__setattr__(self, 'rawFailures', new_raw)
    return value

def _raw_failures_value_set(self, attribute: Attribute, value: Dict[str, int]):
    if value is None:
        raise ValueError(f"{attribute.name} cannot be None")
    new_typed = {}
    for k, v in value.items():
        if k in SendAttemptResult:
            new_typed[SendAttemptResult(k)] = v
    if new_typed != getattr(self, 'failures'):
        object.__setattr__(self, 'failures', new_typed)
    return value

def _raw_failures_default(self) -> Dict[str, int]:
    if self.failures is not None:
        return {k.value: v for k, v in self.failures.items()}
    raise ValueError("Either failures or rawFailures must be provided")

def _validate_raw_failures(self, attribute: Attribute, value: Dict[str, int]):
    if value is None:
        raise ValueError(f"{attribute.name} cannot be None")

@define
class PerformanceTestResultResponse(AttrsRawValueAware):
    """
    An object the API returns that describes the performance test results.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresultresponse
    """

    config: PerformanceTestConfig = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A PerformanceTestConfig object that enumerates the test parameters.

    https://developer.apple.com/documentation/retentionmessaging/performancetestconfig
    """

    failures: Dict[SendAttemptResult, int] = attr.ib(default=None, kw_only=True, on_setattr=_failures_value_set, metadata={metadata_key: 'rawFailures', metadata_type_key: 'main'})
    """
    A Failures object that represents a map of server-to-server notification failure reasons and counts that represent the number of failures encountered during the performance test.

    https://developer.apple.com/documentation/retentionmessaging/failures
    """

    rawFailures: Dict[str, int] = attr.ib(default=attr.Factory(_raw_failures_default, takes_self=True), kw_only=True, on_setattr=_raw_failures_value_set, validator=_validate_raw_failures, metadata={metadata_key: 'failures', metadata_type_key: 'raw', metadata_required_key: True})
    """
    See failures
    """

    numPending: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    An integer that describes the number of pending requests in the performance test.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresultresponse
    """

    responseTimes: PerformanceTestResponseTimes = attr.ib(kw_only=True, validator=validate_not_none)
    """
    A PerformanceTestResponseTimes object that enumerates the response times measured during the test.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresponsetimes
    """

    result: PerformanceTestStatus = PerformanceTestStatus.create_main_attr('rawResult', raw_required=True, kw_only=True)
    """
    A PerformanceTestStatus object that describes the overall result of the test.

    https://developer.apple.com/documentation/retentionmessaging/performanceteststatus
    """

    rawResult: str = PerformanceTestStatus.create_raw_attr('result', required=True)
    """
    See result
    """

    successRate: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    An integer that describes the success rate percentage of the performance test.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresultresponse
    """

    target: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The target URL for the performance test.

    https://developer.apple.com/documentation/retentionmessaging/performancetestresultresponse
    """
