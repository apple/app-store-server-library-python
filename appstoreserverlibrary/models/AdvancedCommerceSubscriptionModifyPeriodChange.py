# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

import attr
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

    effective: AdvancedCommerceEffective = AdvancedCommerceEffective.create_main_attr('rawEffective', raw_required=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/effective
    """

    rawEffective: str = AdvancedCommerceEffective.create_raw_attr('effective', required=True)
    """
    See effective
    """

    period: AdvancedCommercePeriod = AdvancedCommercePeriod.create_main_attr('rawPeriod', raw_required=True)
    """
    https://developer.apple.com/documentation/advancedcommerceapi/period
    """

    rawPeriod: str = AdvancedCommercePeriod.create_raw_attr('period', required=True)
    """
    See period
    """