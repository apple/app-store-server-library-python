# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional, List

from attr import define
import attr

from .GroupType import GroupType
from .LibraryUtility import AttrsRawValueAware
from .RoleEntry import RoleEntry

@define
class GroupEntry(AttrsRawValueAware):
    """
    The identifier, type, and per-product roles for a group that a customer belongs to.

    https://developer.apple.com/documentation/appstoreserverapi/groupentry
    """

    groupId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The identifier of the group.

    https://developer.apple.com/documentation/appstoreserverapi/groupid
    """

    groupType: Optional[GroupType] = GroupType.create_main_attr('rawGroupType', kw_only=True)
    """
    The type of the group.

    https://developer.apple.com/documentation/appstoreserverapi/grouptype
    """

    rawGroupType: Optional[str] = GroupType.create_raw_attr('groupType')
    """
    See groupType
    """

    roles: Optional[List[RoleEntry]] = attr.ib(default=None, kw_only=True)
    """
    An optional array of the customer’s roles in this group, one for each of your products that the group provides access to.

    https://developer.apple.com/documentation/appstoreserverapi/roleentry
    """
