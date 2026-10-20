# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define

from .AdvancedCommerceEffective import AdvancedCommerceEffective
from .AdvancedCommercePeriod import AdvancedCommercePeriod
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceSubscriptionModifyPeriodChange(AttrsRawValueAware):
    """
    The data your app provides to change the period of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmodifyperiodchange
    """

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True, kw_only=True)
    """
    A string value that indicates when a requested change to an auto-renewable subscription goes into effect.

    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    period: AdvancedCommercePeriod = AdvancedCommercePeriod.create_main_attr('rawPeriod', raw_required=True, kw_only=True)
    """
    The duration of a single cycle of an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/period
    """

    rawPeriod: str = AdvancedCommercePeriod.create_raw_attr('period', required=True)
    """
    See period
    """
