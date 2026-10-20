# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AdvancedCommerceOfferPeriod import AdvancedCommerceOfferPeriod
from .AdvancedCommerceOfferReason import AdvancedCommerceOfferReason
from .HelperValidationUtils import HelperValidationUtils
from .LibraryUtility import AttrsRawValueAware, validate_not_none

@define
class AdvancedCommerceOffer(AttrsRawValueAware):
    """
    A discount offer for an auto-renewable subscription.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    period: AdvancedCommerceOfferPeriod = AdvancedCommerceOfferPeriod.create_main_attr('rawPeriod', raw_required=True, kw_only=True)
    """
    The period of the offer.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    rawPeriod: str = AdvancedCommerceOfferPeriod.create_raw_attr('period', required=True)
    """
    See period
    """

    periodCount: int = attr.ib(kw_only=True, validator=HelperValidationUtils.period_count_validator)
    """
    The number of periods the offer is active.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    price: int = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The offer price, in milliunits.

    https://developer.apple.com/documentation/advancedcommerceapi/price
    """

    reason: AdvancedCommerceOfferReason = AdvancedCommerceOfferReason.create_main_attr('rawReason', raw_required=True, kw_only=True)
    """
    The reason for the offer.

    https://developer.apple.com/documentation/advancedcommerceapi/offer
    """

    rawReason: str = AdvancedCommerceOfferReason.create_raw_attr('reason', required=True)
    """
    See reason
    """
