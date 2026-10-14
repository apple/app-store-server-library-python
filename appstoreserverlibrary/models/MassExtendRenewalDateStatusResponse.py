# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

@define
class MassExtendRenewalDateStatusResponse:
    """
    A response that indicates the current status of a request to extend the subscription renewal date to all eligible subscribers.

    https://developer.apple.com/documentation/appstoreserverapi/massextendrenewaldatestatusresponse
    """

    requestIdentifier: Optional[str] = attr.ib(default=None, kw_only=True, validator=attr.validators.optional(attr.validators.max_len(128)))
    """
    The UUID that represents your request for a subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/requestidentifier
    """

    complete: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that’s TRUE to indicate that the App Store completed your request to extend a subscription renewal date for all eligible subscribers.

    https://developer.apple.com/documentation/appstoreserverapi/complete
    """

    completeDate: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The date that the App Store completes the request.

    https://developer.apple.com/documentation/appstoreserverapi/completedate
    """

    failedCount: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The final count of subscribers that fail to receive a subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/failedcount
    """

    succeededCount: Optional[int] = attr.ib(default=None, kw_only=True)
    """
    The final count of subscribers that successfully receive a subscription-renewal-date extension.

    https://developer.apple.com/documentation/appstoreserverapi/succeededcount
    """
