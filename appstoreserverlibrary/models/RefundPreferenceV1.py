# Copyright (c) 2024 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RefundPreferenceV1(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates your preferred outcome for the refund request.

    .. deprecated:: 3.0.0
        Use :class:`RefundPreference` instead.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreferencev1
    """
    UNDECLARED = 0
    """
    The refund preference is undeclared.
    """

    PREFER_GRANT = 1
    """
    You prefer that the App Store grants the refund.
    """

    PREFER_DECLINE = 2
    """
    You prefer that the App Store declines the refund.
    """

    NO_PREFERENCE = 3
    """
    You have no preference whether the App Store grants or declines the refund.
    """
