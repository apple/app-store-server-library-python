# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .HelperValidationUtils import HelperValidationUtils

@define
class TransactionCommitmentInfo:
    """
    https://developer.apple.com/documentation/appstoreserverapi/transactioncommitmentinfo
    """

    billingPeriodNumber: Optional[int] = attr.ib(default=None, validator=attr.validators.optional(HelperValidationUtils.period_count_validator))
    """
    https://developer.apple.com/documentation/appstoreserverapi/billingperiodnumber
    """

    commitmentExpiresDate: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentexpiresdate
    """

    commitmentPrice: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentprice
    """

    totalBillingPeriods: Optional[int] = attr.ib(default=None)
    """
    https://developer.apple.com/documentation/appstoreserverapi/totalbillingperiods
    """
