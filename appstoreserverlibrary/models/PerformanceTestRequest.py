# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

@define
class PerformanceTestRequest:
    """
    The request object you provide for a performance test that contains an original transaction identifier.

    https://developer.apple.com/documentation/retentionmessaging/performancetestrequest
    """

    originalTransactionId: str = attr.ib()
    """
    The original transaction identifier of an In-App Purchase you initiate in the sandbox environment, to use as the purchase for this test.

    https://developer.apple.com/documentation/retentionmessaging/originaltransactionid
    """
