# Copyright (c) 2026 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr

from .AdvancedCommerceOfferPeriod import AdvancedCommerceOfferPeriod
from .AdvancedCommerceOfferReason import AdvancedCommerceOfferReason
from .AdvancedCommerceValidationUtils import AdvancedCommerceValidationUtils
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceOffer(AttrsRawValueAware):
    """
    A discount offer for an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    periodCount: int = attr.ib(validator=AdvancedCommerceValidationUtils.period_count_validator)
    """
    The number of periods the offer is active.
    """

    price: int = attr.ib()
    """
    The offer price, in milliunits.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    period: AdvancedCommerceOfferPeriod = AdvancedCommerceOfferPeriod.create_main_attr('rawPeriod', raw_required=True)
    """
    The period of the offer.
    """

    rawPeriod: str = AdvancedCommerceOfferPeriod.create_raw_attr('period', required=True)
    """
    See period
    """

    reason: AdvancedCommerceOfferReason = AdvancedCommerceOfferReason.create_main_attr('rawReason', raw_required=True)
    """
    The reason for the offer.
    """

    rawReason: str = AdvancedCommerceOfferReason.create_raw_attr('reason', required=True)
    """
    See reason
    """