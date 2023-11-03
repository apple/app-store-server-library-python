# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import Enum

class Environment(str, Enum): 
    """
    The server environment, either sandbox or production.
    
    https://developer.apple.com/documentation/appstoreserverapi/environment
    """
    SANDBOX = "Sandbox"
    PRODUCTION = "Production"
    XCODE = "Xcode"
    LOCAL_TESTING = "LocalTesting"
