# Copyright (c) 2024 Apple Inc. Licensed under MIT License.

from enum import IntEnum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class RefundPreferenceV1(IntEnum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    A value that indicates your preferred outcome for the refund request.

    .. deprecated::
        Use :class:`RefundPreference` instead.

    https://developer.apple.com/documentation/appstoreserverapi/refundpreferencev1
    """
    UNDECLARED = 0
    PREFER_GRANT = 1
    PREFER_DECLINE = 2
    NO_PREFERENCE = 3
