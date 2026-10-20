# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .AutoRenewStatus import AutoRenewStatus
from .LibraryUtility import AttrsRawValueAware
from .RenewalBillingPlanType import RenewalBillingPlanType

@define
class RenewalCommitmentInfo(AttrsRawValueAware):
    """
    https://developer.apple.com/documentation/appstoreserverapi/renewalcommitmentinfo
    """

    commitmentAutoRenewProductId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentautorenewproductid
    """

    commitmentAutoRenewStatus: Optional[AutoRenewStatus] = AutoRenewStatus.create_main_attr('rawCommitmentAutoRenewStatus', kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentautorenewstatus
    """

    rawCommitmentAutoRenewStatus: Optional[int] = AutoRenewStatus.create_raw_attr('commitmentAutoRenewStatus')
    """
    See commitmentAutoRenewStatus
    """

    commitmentRenewalBillingPlanType: Optional[RenewalBillingPlanType] = RenewalBillingPlanType.create_main_attr('rawCommitmentRenewalBillingPlanType', kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentrenewalbillingplantype
    """

    rawCommitmentRenewalBillingPlanType: Optional[str] = RenewalBillingPlanType.create_raw_attr('commitmentRenewalBillingPlanType')
    """
    See commitmentRenewalBillingPlanType
    """

    commitmentRenewalDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentrenewaldate
    """

    commitmentRenewalPrice: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    https://developer.apple.com/documentation/appstoreserverapi/commitmentrenewalprice
    """
