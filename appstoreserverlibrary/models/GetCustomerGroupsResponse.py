# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .GroupEntry import GroupEntry

@define
class GetCustomerGroupsResponse:
    """
    A response that contains the groups a customer belongs to, and their role in each group.

    https://developer.apple.com/documentation/appstoreserverapi/getcustomergroupsresponse
    """

    groups: Optional[List[GroupEntry]] = attr.ib(default=None, kw_only=True)
    """
    An array of groups that the customer belongs to.

    https://developer.apple.com/documentation/appstoreserverapi/groupentry
    """
