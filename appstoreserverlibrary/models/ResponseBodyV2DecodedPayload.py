# Copyright (c) 2023 Apple Inc. Licensed under MIT License.
from typing import Optional

from attr import define
import attr
from .Data import Data

from .NotificationTypeV2 import NotificationTypeV2
from .Subtype import Subtype
from .Summary import Summary


@define
class ResponseBodyV2DecodedPayload: 
    """
    A decoded payload containing the version 2 notification data.
    
    https://developer.apple.com/documentation/appstoreservernotifications/responsebodyv2decodedpayload
    """

    notificationType: Optional[NotificationTypeV2] = attr.ib(default=None)
    """
    The in-app purchase event for which the App Store sends this version 2 notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/notificationtype
    """

    subtype: Optional[Subtype] = attr.ib(default=None)
    """
    Additional information that identifies the notification event. The subtype field is present only for specific version 2 notifications.
    
    https://developer.apple.com/documentation/appstoreservernotifications/subtype
    """

    notificationUUID: Optional[str] = attr.ib(default=None)
    """
    A unique identifier for the notification.
    
    https://developer.apple.com/documentation/appstoreservernotifications/notificationuuid
    """

    data: Optional[Data] = attr.ib(default=None)
    """
    The object that contains the app metadata and signed renewal and transaction information.
    The data and summary fields are mutually exclusive. The payload contains one of the fields, but not both.
    
    https://developer.apple.com/documentation/appstoreservernotifications/data
    """

    version: Optional[str] = attr.ib(default=None)
    """
    A string that indicates the notification's App Store Server Notifications version number.
    
    https://developer.apple.com/documentation/appstoreservernotifications/version
    """

    signedDate: Optional[int] = attr.ib(default=None)
    """
    The UNIX time, in milliseconds, that the App Store signed the JSON Web Signature data.
    
    https://developer.apple.com/documentation/appstoreserverapi/signeddate
    """

    summary: Optional[Summary] = attr.ib(default=None)
    """
    The summary data that appears when the App Store server completes your request to extend a subscription renewal date for eligible subscribers.
    The data and summary fields are mutually exclusive. The payload contains one of the fields, but not both.
    
    https://developer.apple.com/documentation/appstoreservernotifications/summary
    """