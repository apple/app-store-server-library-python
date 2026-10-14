# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import Optional

from attr import define
import attr

from .LibraryUtility import AttrsRawValueAware
from .Role import Role

@define
class RoleEntry(AttrsRawValueAware):
    """
    A customer’s role for a single product within a group.

    https://developer.apple.com/documentation/appstoreserverapi/roleentry
    """

    productId: Optional[str] = attr.ib(default=None, kw_only=True)
    """
    The product identifier of the in-app purchase that the role applies to.

    https://developer.apple.com/documentation/appstoreserverapi/productid
    """

    role: Optional[Role] = Role.create_main_attr('rawRole', kw_only=True)
    """
    The customer’s role for the product.

    https://developer.apple.com/documentation/appstoreserverapi/role
    """

    rawRole: Optional[str] = Role.create_raw_attr('role')
    """
    See role
    """
