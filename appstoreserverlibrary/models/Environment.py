# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

from .LibraryUtility import AppStoreServerLibraryEnumMeta

class Environment(str, Enum, metaclass=AppStoreServerLibraryEnumMeta):
    """
    The server environment, either sandbox or production.

    https://developer.apple.com/documentation/appstoreserverapi/environment
    """
    SANDBOX = "Sandbox"
    """
    Indicates that the data applies to testing in the sandbox environment.
    """

    PRODUCTION = "Production"
    """
    Indicates that the data applies to the production environment.
    """

    XCODE = "Xcode"
    LOCAL_TESTING = "LocalTesting"
