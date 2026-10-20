# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from attr import define
import attr

from .AdvancedCommerceDescriptors import AdvancedCommerceDescriptors
from .HelperValidationUtils import HelperValidationUtils

@define
class AdvancedCommerceSubscriptionMigrateDescriptors(AdvancedCommerceDescriptors):
    """
    The description and display name of the subscription to migrate to that you manage.

    https://developer.apple.com/documentation/advancedcommerceapi/subscriptionmigratedescriptors
    """

    description: str = attr.ib(kw_only=True, validator=HelperValidationUtils.description_validator)
    """
    The description of the subscription to migrate to.

    https://developer.apple.com/documentation/advancedcommerceapi/description
    """

    displayName: str = attr.ib(kw_only=True, validator=HelperValidationUtils.display_name_validator)
    """
    The display name of the subscription to migrate to.

    https://developer.apple.com/documentation/advancedcommerceapi/displayname
    """
