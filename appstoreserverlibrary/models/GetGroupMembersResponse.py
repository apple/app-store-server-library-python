# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .GroupMemberEntry import GroupMemberEntry

@define
class GetGroupMembersResponse:
    """
    A response that contains a page of the customers that belong to a group.

    https://developer.apple.com/documentation/appstoreserverapi/getgroupmembersresponse
    """

    members: Optional[List[GroupMemberEntry]] = attr.ib(default=None, kw_only=True)
    """
    An array of the customers that belong to the group.

    https://developer.apple.com/documentation/appstoreserverapi/groupmemberentry
    """

    paginationToken: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    A token you send in a subsequent request to get the next set of members.

    https://developer.apple.com/documentation/appstoreserverapi/paginationtoken
    """

    hasMore: Optional[bool] = attr.ib(default=None, kw_only=True)
    """
    A Boolean value that indicates whether the group has more members than the response contains.

    https://developer.apple.com/documentation/appstoreserverapi/hasmore
    """
