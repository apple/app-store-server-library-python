# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from abc import ABC

from attr import define
import attr

from .AdvancedCommerceRequest import AdvancedCommerceRequest
from ..jws_signature_creator import AdvancedCommerceInAppRequest

@define
class AbstractAdvancedCommerceInAppRequest(AdvancedCommerceRequest, AdvancedCommerceInAppRequest, ABC):
    operation: str = attr.ib()
    version: str = attr.ib()