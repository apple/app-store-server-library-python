# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from abc import ABC

from attr import define
import attr

from .AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from .LibraryUtility import AttrsRawValueAware

@define
class AdvancedCommerceRequest(AttrsRawValueAware, ABC):
    requestInfo: AdvancedCommerceRequestInfo = attr.ib()
    """
    The metadata to include in server requests.

    https://developer.apple.com/documentation/advancedcommerceapi/requestinfo
    """