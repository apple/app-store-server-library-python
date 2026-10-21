# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

@define
class GroupMemberEntry:
    """
    A customer that belongs to a group.

    https://developer.apple.com/documentation/appstoreserverapi/groupmemberentry
    """

    appTransactionId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The unique identifier of the member’s app download transaction.

    https://developer.apple.com/documentation/appstoreserverapi/apptransactionid
    """
