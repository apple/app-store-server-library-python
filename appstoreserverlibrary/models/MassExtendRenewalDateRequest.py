# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .ExtendReasonCode import ExtendReasonCode
from .LibraryUtility import AttrsRawValueAware, validate_not_none

@define
class MassExtendRenewalDateRequest(AttrsRawValueAware):
    """
    The request body that contains subscription-renewal-extension data to apply for all eligible active subscribers.

    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldaterequest
    """

    requestIdentifier: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(128)])
    """
    A string that contains a one-time UUID value you provide to identify this subscription-renewal-date extension request.

    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    extendByDays: int = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.and_(attr.validators.ge(1), attr.validators.le(90))])
    """
    The number of days to extend the subscription renewal date.

    https://developer.apple.com/documentation/appstoreserverapi/extendbydays
    """

    extendReasonCode: ExtendReasonCode = ExtendReasonCode.create_main_attr('rawExtendReasonCode', raw_required=True, kw_only=True)
    """
    The reason code for the subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """

    rawExtendReasonCode: int = ExtendReasonCode.create_raw_attr('extendReasonCode', required=True)
    """
    See extendReasonCode
    """

    productId: str = attr.ib(kw_only=True, validator=validate_not_none)
    """
    The product identifier of the auto-renewable subscription that you’re requesting the renewal-date extension for.

    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    storefrontCountryCodes: Optional[List[str]] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.deep_iterable(attr.validators.max_len(3))))
    """
    A list of storefront country codes you provide to limit the storefronts that are eligible to receive the subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/storefrontcountrycodes
    """
