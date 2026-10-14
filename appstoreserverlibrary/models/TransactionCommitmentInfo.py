# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

@define
class TransactionCommitmentInfo:
    """
    https://developer.apple.com/documentation/appstoreserverapi/transactioncommitmentinfo
    """

    billingPeriodNumber: Optional[int] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.and_(attr.validators.ge(1), attr.validators.le(12))))
    """
    https://developer.apple.com/documentation/appstoreserverapi/billingperiodnumber
    """

    commitmentExpiresDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentexpiresdate
    """

    commitmentPrice: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentprice
    """

    totalBillingPeriods: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/totalbillingperiods
    """
