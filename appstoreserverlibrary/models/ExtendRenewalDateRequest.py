# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .ExtendReasonCode import ExtendReasonCode
from .LibraryUtility import AttrsRawValueAware, validate_not_none

@define
class ExtendRenewalDateRequest(AttrsRawValueAware):
    """
    The request body that contains subscription-renewal-extension data for an individual subscription.

    https://developer.apple.com/documentation/appstoreserverapi/extendrenewaldaterequest
    """

    extendByDays: int = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.and_(attr.validators.ge(1), attr.validators.le(90))])
    """
    The number of days to extend the subscription renewal date.

    https://developer.apple.com/documentation/appstoreserverapi/extendbydays
    """

    extendReasonCode: ExtendReasonCode = ExtendReasonCode.create_main_attr('rawExtendReasonCode', raw_required=True, kw_only=True)
    """
    The reason code for the subscription date extension.

    https://developer.apple.com/documentation/appstoreserverapi/extendreasoncode
    """

    rawExtendReasonCode: int = ExtendReasonCode.create_raw_attr('extendReasonCode', required=True)
    """
    See extendReasonCode
    """

    requestIdentifier: str = attr.ib(kw_only=True, validator=[validate_not_none, attr.validators.max_len(128)])
    """
    A string that contains a value you provide to uniquely identify this renewal-date extension request.

    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """
