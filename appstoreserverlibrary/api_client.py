# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import calendar
import datetime
from enum import Enum
from typing import Dict, List, Optional, Type, TypeVar, Union
from attr import define
import cattrs
import requests

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from .models.CheckTestNotificationResponse import CheckTestNotificationResponse
from .models.ConsumptionRequest import ConsumptionRequest

from .models.Environment import Environment
from .models.ExtendRenewalDateRequest import ExtendRenewalDateRequest
from .models.ExtendRenewalDateResponse import ExtendRenewalDateResponse
from .models.HistoryResponse import HistoryResponse
from .models.MassExtendRenewalDateRequest import MassExtendRenewalDateRequest
from .models.MassExtendRenewalDateResponse import MassExtendRenewalDateResponse
from .models.MassExtendRenewalDateStatusResponse import MassExtendRenewalDateStatusResponse
from .models.OrderLookupResponse import OrderLookupResponse
from .models.RefundHistoryResponse import RefundHistoryResponse
from .models.SendTestNotificationResponse import SendTestNotificationResponse
from .models.Status import Status
from .models.StatusResponse import StatusResponse
from .models.TransactionHistoryRequest import TransactionHistoryRequest
from .models.TransactionInfoResponse import TransactionInfoResponse

T = TypeVar('T')

class APIError(Enum):
    GENERAL_BAD_REQUEST = 4000000
    INVALID_APP_IDENTIFIER = 4000002
    INVALID_REQUEST_REVISION = 4000005
    INVALID_TRANSACTION_ID = 4000006
    INVALID_ORIGINAL_TRANSACTION_ID = 4000008
    INVALID_EXTEND_BY_DAYS = 4000009
    INVALID_EXTEND_REASON_CODE = 4000010
    INVALID_IDENTIFIER = 4000011
    START_DATE_TOO_FAR_IN_PAST = 4000012
    START_DATE_AFTER_END_DATE = 4000013
    INVALID_PAGINATION_TOKEN = 4000014
    INVALID_START_DATE = 4000015
    INVALID_END_DATE = 4000016
    PAGINATION_TOKEN_EXPIRED = 4000017
    INVALID_NOTIFICATION_TYPE = 4000018
    MULTIPLE_FILTERS_SUPPLIED = 4000019
    INVALID_TEST_NOTIFICATION_TOKEN = 4000020
    INVALID_SORT = 4000021
    INVALID_PRODUCT_TYPE = 4000022
    INVALID_PRODUCT_ID = 4000023
    INVALID_SUBSCRIPTION_GROUP_IDENTIFIER = 4000024
    INVALID_EXCLUDE_REVOKED = 4000025
    INVALID_IN_APP_OWNERSHIP_TYPE = 4000026
    INVALID_EMPTY_STOREFRONT_COUNTRY_CODE_LIST = 4000027
    INVALID_STOREFRONT_COUNTRY_CODE = 4000028
    INVALID_REVOKED = 4000030
    INVALID_STATUS = 4000031
    SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030004
    SUBSCRIPTION_MAX_EXTENSION = 4030005
    FAMILY_SHARED_SUBSCRIPTION_EXTENSION_INELIGIBLE = 4030007
    ACCOUNT_NOT_FOUND = 4040001
    ACCOUNT_NOT_FOUND_RETRYABLE = 4040002
    APP_NOT_FOUND = 4040003
    APP_NOT_FOUND_RETRYABLE = 4040004
    ORIGINAL_TRANSACTION_ID_NOT_FOUND = 4040005
    ORIGINAL_TRANSACTION_ID_NOT_FOUND_RETRYABLE = 4040006
    SERVER_NOTIFICATION_URL_NOT_FOUND = 4040007
    TEST_NOTIFICATION_NOT_FOUND = 4040008
    STATUS_REQUEST_NOT_FOUND = 4040009
    TRANSACTION_ID_NOT_FOUND = 4040010
    RATE_LIMIT_EXCEEDED = 4290000
    GENERAL_INTERNAL = 5000000
    GENERAL_INTERNAL_RETRYABLE = 5000001


@define
class APIException(Exception):
    http_status_code: int
    api_error: APIError

    def __init__(self, http_status_code: int, api_error: APIError = None):
        self.http_status_code = http_status_code
        self.api_error = api_error

class AppStoreServerAPIClient:
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str, environment: Environment):
        if environment == Environment.PRODUCTION:
            self._base_url = "https://api.storekit.itunes.apple.com"
        else:
            self._base_url = "https://api.storekit-sandbox.itunes.apple.com"
        self._signing_key = serialization.load_pem_private_key(signing_key, password=None, backend=default_backend())
        self._key_id = key_id
        self._issuer_id = issuer_id
        self._bundle_id = bundle_id

    def _generate_token(self) -> str:
        future_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        return jwt.encode(
            {
                "bid": self._bundle_id,
                "iss": self._issuer_id,
                "aud": "appstoreconnect-v1",
                "exp": calendar.timegm(future_time.timetuple()),
            },
            self._signing_key,
            algorithm="ES256",
            headers={"kid": self._key_id},
        )

    def _make_request(self, path: str, method: str, queryParameters: Dict[str, Union[str, List[str]]], body, destination_class: Type[T]) -> T:
        url = self._base_url + path
        json = cattrs.unstructure(body) if body != None else None
        headers = {
            'User-Agent': "app-store-server-library/python/0.1",
            'Authorization': 'Bearer ' + self._generate_token(),
            'Accept': 'application/json'
        }
        
        response = requests.request(method, url, params=queryParameters, headers=headers, json=json)
        if response.status_code >= 200 and response.status_code < 300:
            if destination_class == None:
                return
            response_body = response.json()
            return cattrs.structure(response_body, destination_class)
        else:
            # Best effort parsing of the response body
            if not 'content-type' in response.headers or response.headers['content-type'] != 'application/json':
                raise APIException(response.status_code)
            try:
                response_body = response.json()
                errorValue = APIError(response_body['errorCode'])
                raise APIException(response.status_code, errorValue)
            except APIException as e:
                raise e
            except Exception:
                raise APIException(response.status_code)

    
    def extend_renewal_date_for_all_active_subscribers(self, mass_extend_renewal_date_request: MassExtendRenewalDateRequest) -> MassExtendRenewalDateResponse: 
        """
        Uses a subscription's product identifier to extend the renewal date for all of its eligible active subscribers.
        
        :param mass_extend_renewal_date_request The request body for extending a subscription renewal date for all of its active subscribers.
        :return A response that indicates the server successfully received the subscription-renewal-date extension request.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/extend_subscription_renewal_dates_for_all_active_subscribers
        """
        return self._make_request("/inApps/v1/subscriptions/extend/mass/", "POST", {}, mass_extend_renewal_date_request, MassExtendRenewalDateResponse)

    def extend_subscription_renewal_date(self, original_transaction_id: str, extend_renewal_date_request: ExtendRenewalDateRequest) -> ExtendRenewalDateResponse:
        """
        Extends the renewal date of a customer's active subscription using the original transaction identifier.
        
        :param original_transaction_id    The original transaction identifier of the subscription receiving a renewal date extension.
        :param extend_renewal_date_request The request body containing subscription-renewal-extension data.
        :return A response that indicates whether an individual renewal-date extension succeeded, and related details.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/extend_a_subscription_renewal_date
        """
        return self._make_request("/inApps/v1/subscriptions/extend/" + original_transaction_id, "PUT", {}, extend_renewal_date_request, ExtendRenewalDateResponse)
    
    def get_all_subscription_statuses(self, transaction_id: str, status: List[Status] = None) -> StatusResponse:
        """
        Get the statuses for all of a customer's auto-renewable subscriptions in your app.
        
        :param transaction_id The identifier of a transaction that belongs to the customer, and which may be an original transaction identifier.
        :param status An optional filter that indicates the status of subscriptions to include in the response. Your query may specify more than one status query parameter.
        :return A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/get_all_subscription_statuses
        """
        queryParameters: Dict[str, List[str]] = dict()
        if status != None:
            queryParameters["status"] = [s.value for s in status]
        
        return self._make_request("/inApps/v1/subscriptions/" + transaction_id, "GET", queryParameters, None, StatusResponse)
    
    def get_refund_history(self, transaction_id: str, revision: str) -> RefundHistoryResponse:
        """
        Get a paginated list of all of a customer's refunded in-app purchases for your app.
        
        :param transaction_id The identifier of a transaction that belongs to the customer, and which may be an original transaction identifier.
        :param revision              A token you provide to get the next set of up to 20 transactions. All responses include a revision token. Use the revision token from the previous RefundHistoryResponse.
        :return A response that contains status information for all of a customer's auto-renewable subscriptions in your app.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/get_refund_history
        """

        queryParameters: Dict[str, List[str]] = dict()
        if revision != None:
            queryParameters["revision"] = [revision]
        
        return self._make_request("/inApps/v2/refund/lookup/" + transaction_id, "GET", queryParameters, None, RefundHistoryResponse)
    
    def get_status_of_subscription_renewal_date_extensions(self, request_identifier: str, product_id: str) -> MassExtendRenewalDateStatusResponse:
        """
        Checks whether a renewal date extension request completed, and provides the final count of successful or failed extensions.
        
        :param request_identifier The UUID that represents your request to the Extend Subscription Renewal Dates for All Active Subscribers endpoint.
        :param product_id         The product identifier of the auto-renewable subscription that you request a renewal-date extension for.
        :return A response that indicates the current status of a request to extend the subscription renewal date to all eligible subscribers.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/get_status_of_subscription_renewal_date_extensions
        """
        return self._make_request("/inApps/v1/subscriptions/extend/mass/" + product_id + "/" + request_identifier, "GET", {}, None, MassExtendRenewalDateStatusResponse)
    
    def get_test_notification_status(self, test_notification_token: str) -> CheckTestNotificationResponse:
        """
        Check the status of the test App Store server notification sent to your server.
        
        :param test_notification_token The test notification token received from the Request a Test Notification endpoint
        :return A response that contains the contents of the test notification sent by the App Store server and the result from your server.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/get_test_notification_status
        """
        return self._make_request("/inApps/v1/notifications/test/" + test_notification_token, "GET", {}, None, CheckTestNotificationResponse)
    
    def get_transaction_history(self, transaction_id: str, revision: Optional[str], transaction_history_request: TransactionHistoryRequest) -> HistoryResponse:
        """
        Get a customer's in-app purchase transaction history for your app.
        
        :param transaction_id The identifier of a transaction that belongs to the customer, and which may be an original transaction identifier.
        :param revision              A token you provide to get the next set of up to 20 transactions. All responses include a revision token. Note: For requests that use the revision token, include the same query parameters from the initial request. Use the revision token from the previous HistoryResponse.
        :return A response that contains the customer's transaction history for an app.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/get_transaction_history
        """
        queryParameters: Dict[str, List[str]] = dict()
        if revision != None:
            queryParameters["revision"] = [revision]
        
        if transaction_history_request.startDate != None:
            queryParameters["startDate"] = [str(transaction_history_request.startDate)]
        
        if transaction_history_request.endDate != None:
            queryParameters["endDate"] = [str(transaction_history_request.endDate)]
        
        if transaction_history_request.productIds != None:
            queryParameters["product_id"] = transaction_history_request.productIds
        
        if transaction_history_request.productTypes != None:
            queryParameters["productType"] = [product_type.value for product_type in transaction_history_request.productTypes]
        
        if transaction_history_request.sort != None:
            queryParameters["sort"] = [transaction_history_request.sort.value]
        
        if transaction_history_request.subscriptionGroupIdentifiers != None:
            queryParameters["subscriptionGroupIdentifier"] = transaction_history_request.subscriptionGroupIdentifiers
        
        if transaction_history_request.inAppOwnershipType != None:
            queryParameters["inAppOwnershipType"] = [transaction_history_request.inAppOwnershipType.value]
        
        if transaction_history_request.revoked != None:
            queryParameters["revoked"] = [str(transaction_history_request.revoked)]
        
        return self._make_request("/inApps/v1/history/" + transaction_id, "GET", queryParameters, None, HistoryResponse)
    
    def get_transaction_info(self, transaction_id: str) -> TransactionInfoResponse:
        """
        Get information about a single transaction for your app.
        
        :param transaction_id The identifier of a transaction that belongs to the customer, and which may be an original transaction identifier.
        :return A response that contains signed transaction information for a single transaction.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/get_transaction_info
        """
        return self._make_request("/inApps/v1/transactions/" + transaction_id, "GET", {}, None, TransactionInfoResponse)

    def look_up_order_id(self, order_id: str) -> OrderLookupResponse:
        """
        Get a customer's in-app purchases from a receipt using the order ID.
        
        :param order_id The order ID for in-app purchases that belong to the customer.
        :return A response that includes the order lookup status and an array of signed transactions for the in-app purchases in the order.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/look_up_order_id
        """
        return self._make_request("/inApps/v1/lookup/" + order_id, "GET", {}, None, OrderLookupResponse)
    def request_test_notification(self) -> SendTestNotificationResponse:
        """
        Ask App Store Server Notifications to send a test notification to your server.
        
        :return A response that contains the test notification token.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/request_a_test_notification
        """
        return self._make_request("/inApps/v1/notifications/test", "POST", {}, None, SendTestNotificationResponse)
        
    def send_consumption_data(self, transaction_id: str, consumption_request: ConsumptionRequest):
        """
        Send consumption information about a consumable in-app purchase to the App Store after your server receives a consumption request notification.
        
        :param transaction_id The transaction identifier for which you’re providing consumption information. You receive this identifier in the CONSUMPTION_REQUEST notification the App Store sends to your server.
        :param consumption_request    The request body containing consumption information.
        :throws APIException If a response was returned indicating the request could not be processed
        https://developer.apple.com/documentation/appstoreserverapi/send_consumption_information
        """
        self._make_request("/inApps/v1/transactions/consumption/" + transaction_id, "PUT", {}, consumption_request, None)
    