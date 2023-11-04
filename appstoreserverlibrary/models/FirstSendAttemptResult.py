# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum, unique

from .LibraryUtility import AppStoreServerLibraryEnumMeta

@unique
class FirstSendAttemptResult(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    An error or result that the App Store server receives when attempting to send an App Store server notification to your server.
    
    https://developer.apple.com/documentation/appstoreserverapi/firstsendattemptresult
    """
    SUCCESS = "SUCCESS"
    TIMED_OUT = "TIMED_OUT"
    TLS_ISSUE = "TLS_ISSUE"
    CIRCULAR_REDIRECT = "CIRCULAR_REDIRECT"
    NO_RESPONSE = "NO_RESPONSE"
    SOCKET_ISSUE = "SOCKET_ISSUE"
    UNSUPPORTED_CHARSET = "UNSUPPORTED_CHARSET"
    INVALID_RESPONSE = "INVALID_RESPONSE"
    PREMATURE_CLOSE = "PREMATURE_CLOSE"
    UNSUCCESSFUL_HTTP_RESPONSE_CODE = "UNSUCCESSFUL_HTTP_RESPONSE_CODE"
    OTHER = "OTHER"
