# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Any, Dict, List, Union
import unittest

from httpx import Response

from appstoreserverlibrary.api_client import APIError, APIException, AsyncAppStoreServerAPIClient, GetTransactionHistoryVersion
from appstoreserverlibrary.models.AccountTenure import AccountTenure
from appstoreserverlibrary.models.AutoRenewStatus import AutoRenewStatus
from appstoreserverlibrary.models.ConsumptionRequest import ConsumptionRequest
from appstoreserverlibrary.models.ConsumptionStatus import ConsumptionStatus
from appstoreserverlibrary.models.DeliveryStatus import DeliveryStatus
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.ExpirationIntent import ExpirationIntent
from appstoreserverlibrary.models.ExtendReasonCode import ExtendReasonCode
from appstoreserverlibrary.models.ExtendRenewalDateRequest import ExtendRenewalDateRequest
from appstoreserverlibrary.models.InAppOwnershipType import InAppOwnershipType
from appstoreserverlibrary.models.LastTransactionsItem import LastTransactionsItem
from appstoreserverlibrary.models.LifetimeDollarsPurchased import LifetimeDollarsPurchased
from appstoreserverlibrary.models.LifetimeDollarsRefunded import LifetimeDollarsRefunded
from appstoreserverlibrary.models.MassExtendRenewalDateRequest import MassExtendRenewalDateRequest
from appstoreserverlibrary.models.NotificationHistoryRequest import NotificationHistoryRequest
from appstoreserverlibrary.models.NotificationHistoryResponseItem import NotificationHistoryResponseItem
from appstoreserverlibrary.models.NotificationTypeV2 import NotificationTypeV2
from appstoreserverlibrary.models.OfferType import OfferType
from appstoreserverlibrary.models.OrderLookupStatus import OrderLookupStatus
from appstoreserverlibrary.models.Platform import Platform
from appstoreserverlibrary.models.PlayTime import PlayTime
from appstoreserverlibrary.models.PriceIncreaseStatus import PriceIncreaseStatus
from appstoreserverlibrary.models.RefundPreference import RefundPreference
from appstoreserverlibrary.models.RevocationReason import RevocationReason
from appstoreserverlibrary.models.SendAttemptItem import SendAttemptItem
from appstoreserverlibrary.models.SendAttemptResult import SendAttemptResult
from appstoreserverlibrary.models.Status import Status
from appstoreserverlibrary.models.SubscriptionGroupIdentifierItem import SubscriptionGroupIdentifierItem
from appstoreserverlibrary.models.Subtype import Subtype
from appstoreserverlibrary.models.TransactionHistoryRequest import Order, ProductType, TransactionHistoryRequest
from appstoreserverlibrary.models.TransactionReason import TransactionReason
from appstoreserverlibrary.models.Type import Type
from appstoreserverlibrary.models.UserStatus import UserStatus

from tests.util import decode_json_from_signed_date, read_data_from_binary_file, read_data_from_file

from io import BytesIO

class DecodedPayloads(unittest.IsolatedAsyncioTestCase):
    async def test_extend_renewal_date_for_all_active_subscribers(self):
        client = self.get_client_with_body_from_file('tests/resources/models/extendRenewalDateForAllActiveSubscribersResponse.json',
                                           'POST',
                                           'https://local-testing-base-url/inApps/v1/subscriptions/extend/mass',
                                           {}, 
                                           {'extendByDays': 45, 'extendReasonCode': 1, 'requestIdentifier': 'fdf964a4-233b-486c-aac1-97d8d52688ac', 'storefrontCountryCodes': ['USA', 'MEX'], 'productId': 'com.example.productId'})
        
        extend_renewal_date_request = MassExtendRenewalDateRequest(
             extendByDays=45,
             extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION,
             requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac',
             storefrontCountryCodes=['USA', 'MEX'],
             productId='com.example.productId')

        mass_extend_renewal_date_response = await client.extend_renewal_date_for_all_active_subscribers(extend_renewal_date_request)

        self.assertIsNotNone(mass_extend_renewal_date_response)
        self.assertEqual('758883e8-151b-47b7-abd0-60c4d804c2f5', mass_extend_renewal_date_response.requestIdentifier)

    async def test_extend_subscription_renewal_date(self):
        client = self.get_client_with_body_from_file('tests/resources/models/extendSubscriptionRenewalDateResponse.json',
                                           'PUT',
                                           'https://local-testing-base-url/inApps/v1/subscriptions/extend/4124214',
                                           {},
                                           {'extendByDays': 45, 'extendReasonCode': 1, 'requestIdentifier': 'fdf964a4-233b-486c-aac1-97d8d52688ac'})

        extend_renewal_date_request = ExtendRenewalDateRequest(
             extendByDays=45,
             extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION,
             requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac'
        )

        extend_renewal_date_response = await client.extend_subscription_renewal_date('4124214', extend_renewal_date_request)

        self.assertIsNotNone(extend_renewal_date_response)
        self.assertEqual('2312412', extend_renewal_date_response.originalTransactionId)
        self.assertEqual('9993', extend_renewal_date_response.webOrderLineItemId)
        self.assertTrue(extend_renewal_date_response.success)
        self.assertEqual(1698148900000, extend_renewal_date_response.effectiveDate)

    async def test_get_all_subscription_statuses(self):
        client = self.get_client_with_body_from_file('tests/resources/models/getAllSubscriptionStatusesResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/subscriptions/4321', 
                                           {'status': [2, 1]},
                                           None)

        status_response = await client.get_all_subscription_statuses('4321', [Status.EXPIRED, Status.ACTIVE])

        self.assertIsNotNone(status_response)
        self.assertEqual(Environment.LOCAL_TESTING, status_response.environment)
        self.assertEqual('LocalTesting', status_response.rawEnvironment)
        self.assertEqual('com.example', status_response.bundleId)
        self.assertEqual(5454545, status_response.appAppleId)


        expected_body = [
             SubscriptionGroupIdentifierItem(
                subscriptionGroupIdentifier='sub_group_one',
                lastTransactions=[
                    LastTransactionsItem(
                        status=Status.ACTIVE,
                        originalTransactionId='3749183',
                        signedTransactionInfo='signed_transaction_one',
                        signedRenewalInfo='signed_renewal_one'
                    ),
                    LastTransactionsItem(
                        status=Status.REVOKED,
                        originalTransactionId='5314314134',
                        signedTransactionInfo='signed_transaction_two',
                        signedRenewalInfo='signed_renewal_two'
                    )
                ]
            ),
            SubscriptionGroupIdentifierItem(
                 subscriptionGroupIdentifier='sub_group_two',
                 lastTransactions=[
                      LastTransactionsItem(
                           status=Status.EXPIRED,
                           originalTransactionId='3413453',
                           signedTransactionInfo='signed_transaction_three',
                           signedRenewalInfo='signed_renewal_three'
                      )
                 ]
            )
        ]
        self.assertEqual(expected_body, status_response.data)

    async def test_get_refund_history(self):
        client = self.get_client_with_body_from_file('tests/resources/models/getRefundHistoryResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v2/refund/lookup/555555', 
                                           {'revision': ['revision_input']}, 
                                           None)

        refund_history_response = await client.get_refund_history('555555', 'revision_input')

        self.assertIsNotNone(refund_history_response)
        self.assertEqual(['signed_transaction_one', 'signed_transaction_two'], refund_history_response.signedTransactions)
        self.assertEqual('revision_output', refund_history_response.revision)
        self.assertTrue(refund_history_response.hasMore)

    async def test_get_status_of_subscription_renewal_date_extensions(self):
        client = self.get_client_with_body_from_file('tests/resources/models/getStatusOfSubscriptionRenewalDateExtensionsResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/subscriptions/extend/mass/20fba8a0-2b80-4a7d-a17f-85c1854727f8/com.example.product', 
                                           {},
                                           None)

        mass_extend_renewal_date_status_response = await client.get_status_of_subscription_renewal_date_extensions('com.example.product', '20fba8a0-2b80-4a7d-a17f-85c1854727f8')

        self.assertIsNotNone(mass_extend_renewal_date_status_response)
        self.assertEqual('20fba8a0-2b80-4a7d-a17f-85c1854727f8', mass_extend_renewal_date_status_response.requestIdentifier)
        self.assertTrue(mass_extend_renewal_date_status_response.complete)
        self.assertEqual(1698148900000, mass_extend_renewal_date_status_response.completeDate)
        self.assertEqual(30, mass_extend_renewal_date_status_response.succeededCount)
        self.assertEqual(2, mass_extend_renewal_date_status_response.failedCount)

    async def test_get_test_notification_status(self):
        client = self.get_client_with_body_from_file('tests/resources/models/getTestNotificationStatusResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/notifications/test/8cd2974c-f905-492a-bf9a-b2f47c791d19',
                                           {},
                                           None)

        check_test_notification_response = await client.get_test_notification_status('8cd2974c-f905-492a-bf9a-b2f47c791d19')

        self.assertIsNotNone(check_test_notification_response)
        self.assertEqual('signed_payload', check_test_notification_response.signedPayload)
        sendAttemptItems = [
                                SendAttemptItem(attemptDate=1698148900000,sendAttemptResult=SendAttemptResult.NO_RESPONSE),
                                SendAttemptItem(attemptDate=1698148950000,sendAttemptResult=SendAttemptResult.SUCCESS)
                            ]
        self.assertEqual(sendAttemptItems, check_test_notification_response.sendAttempts)

    async def test_get_notification_history(self):
        client = self.get_client_with_body_from_file('tests/resources/models/getNotificationHistoryResponse.json',
                                           'POST',
                                           'https://local-testing-base-url/inApps/v1/notifications/history', 
                                           {'paginationToken': ['a036bc0e-52b8-4bee-82fc-8c24cb6715d6']},
                                           {'startDate': 1698148900000, 'endDate': 1698148950000, 'notificationType': 'SUBSCRIBED', 'notificationSubtype': 'INITIAL_BUY', 'transactionId': '999733843', 'onlyFailures': True})

        notification_history_request = NotificationHistoryRequest(
            startDate=1698148900000,
            endDate=1698148950000,
            notificationType=NotificationTypeV2.SUBSCRIBED,
            notificationSubtype=Subtype.INITIAL_BUY,
            transactionId='999733843',
            onlyFailures=True
        )
        
        notification_history_response = await client.get_notification_history('a036bc0e-52b8-4bee-82fc-8c24cb6715d6', notification_history_request)

        self.assertIsNotNone(notification_history_response)
        self.assertEqual('57715481-805a-4283-8499-1c19b5d6b20a', notification_history_response.paginationToken)
        self.assertTrue(notification_history_response.hasMore)
        expected_notification_history = [
             NotificationHistoryResponseItem(sendAttempts=[
                  SendAttemptItem(
                       attemptDate=1698148900000,
                       sendAttemptResult=SendAttemptResult.NO_RESPONSE
                  ),
                  SendAttemptItem(
                       attemptDate=1698148950000,
                       rawSendAttemptResult='SUCCESS'
                  )
             ], signedPayload='signed_payload_one'),
             NotificationHistoryResponseItem(sendAttempts=[
                  SendAttemptItem(
                       attemptDate=1698148800000,
                        sendAttemptResult=SendAttemptResult.CIRCULAR_REDIRECT
                    )
             ], signedPayload='signed_payload_two')
        ]
        self.assertEqual(expected_notification_history, notification_history_response.notificationHistory)

    async def test_get_transaction_history_v1(self):
        client = self.get_client_with_body_from_file('tests/resources/models/transactionHistoryResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/history/1234', 
                                           {'revision': ['revision_input'],
                                            'startDate': ['123455'],
                                            'endDate': ['123456'],
                                            'productId': ['com.example.1', 'com.example.2'],
                                            'productType': ['CONSUMABLE', 'AUTO_RENEWABLE'],
                                            'sort': ['ASCENDING'],
                                            'subscriptionGroupIdentifier': ['sub_group_id', 'sub_group_id_2'],
                                            'inAppOwnershipType': ['FAMILY_SHARED'],
                                            'revoked': ['False']},
                                            None)

        request = TransactionHistoryRequest(
            sort=Order.ASCENDING,
            productTypes=[ProductType.CONSUMABLE, ProductType.AUTO_RENEWABLE],
            endDate=123456,
            startDate=123455,
            revoked=False,
            inAppOwnershipType=InAppOwnershipType.FAMILY_SHARED,
            productIds=['com.example.1', 'com.example.2'],
            subscriptionGroupIdentifiers=['sub_group_id', 'sub_group_id_2']
        )

        history_response = await client.get_transaction_history('1234', 'revision_input', request, GetTransactionHistoryVersion.V1)

        self.assertIsNotNone(history_response)
        self.assertEqual('revision_output', history_response.revision)
        self.assertTrue(history_response.hasMore)
        self.assertEqual('com.example', history_response.bundleId)
        self.assertEqual(323232, history_response.appAppleId)
        self.assertEqual(Environment.LOCAL_TESTING, history_response.environment)
        self.assertEqual('LocalTesting', history_response.rawEnvironment)
        self.assertEqual(['signed_transaction_value', 'signed_transaction_value2'], history_response.signedTransactions)

    async def test_get_transaction_history_v2(self):
        client = self.get_client_with_body_from_file('tests/resources/models/transactionHistoryResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v2/history/1234', 
                                           {'revision': ['revision_input'],
                                            'startDate': ['123455'],
                                            'endDate': ['123456'],
                                            'productId': ['com.example.1', 'com.example.2'],
                                            'productType': ['CONSUMABLE', 'AUTO_RENEWABLE'],
                                            'sort': ['ASCENDING'],
                                            'subscriptionGroupIdentifier': ['sub_group_id', 'sub_group_id_2'],
                                            'inAppOwnershipType': ['FAMILY_SHARED'],
                                            'revoked': ['False']},
                                            None)

        request = TransactionHistoryRequest(
            sort=Order.ASCENDING,
            productTypes=[ProductType.CONSUMABLE, ProductType.AUTO_RENEWABLE],
            endDate=123456,
            startDate=123455,
            revoked=False,
            inAppOwnershipType=InAppOwnershipType.FAMILY_SHARED,
            productIds=['com.example.1', 'com.example.2'],
            subscriptionGroupIdentifiers=['sub_group_id', 'sub_group_id_2']
        )

        history_response = await client.get_transaction_history('1234', 'revision_input', request, GetTransactionHistoryVersion.V2)

        self.assertIsNotNone(history_response)
        self.assertEqual('revision_output', history_response.revision)
        self.assertTrue(history_response.hasMore)
        self.assertEqual('com.example', history_response.bundleId)
        self.assertEqual(323232, history_response.appAppleId)
        self.assertEqual(Environment.LOCAL_TESTING, history_response.environment)
        self.assertEqual('LocalTesting', history_response.rawEnvironment)
        self.assertEqual(['signed_transaction_value', 'signed_transaction_value2'], history_response.signedTransactions)

    async def test_get_transaction_info(self):
        client = self.get_client_with_body_from_file('tests/resources/models/transactionInfoResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/transactions/1234', 
                                           {},
                                           None)

        transaction_info_response = await client.get_transaction_info('1234')

        self.assertIsNotNone(transaction_info_response)
        self.assertEqual('signed_transaction_info_value', transaction_info_response.signedTransactionInfo)

    async def test_look_up_order_id(self):
        client = self.get_client_with_body_from_file('tests/resources/models/lookupOrderIdResponse.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/lookup/W002182',
                                           {},
                                           None)

        order_lookup_response = await client.look_up_order_id('W002182')

        self.assertIsNotNone(order_lookup_response)
        self.assertEqual(OrderLookupStatus.INVALID, order_lookup_response.status)
        self.assertEqual(1, order_lookup_response.rawStatus)
        self.assertEqual(['signed_transaction_one', 'signed_transaction_two'], order_lookup_response.signedTransactions)

    async def test_request_test_notification(self):
        client = self.get_client_with_body_from_file('tests/resources/models/requestTestNotificationResponse.json',
                                           'POST',
                                           'https://local-testing-base-url/inApps/v1/notifications/test',
                                           {},
                                           None)

        send_test_notification_response = await client.request_test_notification()

        self.assertIsNotNone(send_test_notification_response)
        self.assertEqual('ce3af791-365e-4c60-841b-1674b43c1609', send_test_notification_response.testNotificationToken)

    async def test_send_consumption_data(self):
        client = self.get_client_with_body(b'',
                                           'PUT',
                                           'https://local-testing-base-url/inApps/v1/transactions/consumption/49571273', 
                                           {},
                                           {'customerConsented': True,
                                            'consumptionStatus': 1,
                                            'platform': 2,
                                            'sampleContentProvided': False,
                                            'deliveryStatus': 3,
                                            'appAccountToken': '7389a31a-fb6d-4569-a2a6-db7d85d84813',
                                            'accountTenure': 4,
                                            'playTime': 5,
                                            'lifetimeDollarsRefunded': 6,
                                            'lifetimeDollarsPurchased': 7,
                                            'userStatus': 4,
                                            'refundPreference': 3})

        consumptionRequest = ConsumptionRequest(
            customerConsented=True,
            consumptionStatus=ConsumptionStatus.NOT_CONSUMED,
            platform=Platform.NON_APPLE,
            sampleContentProvided=False,
            deliveryStatus=DeliveryStatus.DID_NOT_DELIVER_DUE_TO_SERVER_OUTAGE,
            appAccountToken='7389a31a-fb6d-4569-a2a6-db7d85d84813',
            accountTenure=AccountTenure.THIRTY_DAYS_TO_NINETY_DAYS,
            playTime=PlayTime.ONE_DAY_TO_FOUR_DAYS,
            lifetimeDollarsRefunded=LifetimeDollarsRefunded.ONE_THOUSAND_DOLLARS_TO_ONE_THOUSAND_NINE_HUNDRED_NINETY_NINE_DOLLARS_AND_NINETY_NINE_CENTS,
            lifetimeDollarsPurchased=LifetimeDollarsPurchased.TWO_THOUSAND_DOLLARS_OR_GREATER,
            userStatus=UserStatus.LIMITED_ACCESS,
            refundPreference=RefundPreference.NO_PREFERENCE
        )

        await client.send_consumption_data('49571273', consumptionRequest)

    async def test_api_error(self):
        client = self.get_client_with_body_from_file('tests/resources/models/apiException.json',
                                                     'POST',
                                                     'https://local-testing-base-url/inApps/v1/notifications/test',
                                                     {},
                                                     None,
                                                     500)
        try:
            await client.request_test_notification()
        except APIException as e:
            self.assertEqual(500, e.http_status_code)
            self.assertEqual(5000000, e.raw_api_error)
            self.assertEqual(APIError.GENERAL_INTERNAL, e.api_error)
            self.assertEqual("An unknown error occurred.", e.error_message)
            return
        
        self.assertFalse(True)

    async def test_xcode_not_supported_error(self):
        try:
            signing_key = self.get_signing_key()
            AsyncAppStoreServerAPIClient(signing_key, 'keyId', 'issuerId', 'com.example', Environment.XCODE)
        except ValueError as e:
            self.assertEqual("Xcode is not a supported environment for an AppStoreServerAPIClient", e.args[0])
            return

        self.assertFalse(True)
    
    async def test_api_too_many_requests(self):
        client = self.get_client_with_body_from_file('tests/resources/models/apiTooManyRequestsException.json',
                                                     'POST',
                                                     'https://local-testing-base-url/inApps/v1/notifications/test',
                                                     {},
                                                     None,
                                                     429)
        try:
            await client.request_test_notification()
        except APIException as e:
            self.assertEqual(429, e.http_status_code)
            self.assertEqual(4290000, e.raw_api_error)
            self.assertEqual(APIError.RATE_LIMIT_EXCEEDED, e.api_error)
            self.assertEqual("Rate limit exceeded.", e.error_message)
            return
        
        self.assertFalse(True)

    async def test_unknown_error(self):
        client = self.get_client_with_body_from_file('tests/resources/models/apiUnknownError.json',
                                                     'POST',
                                                     'https://local-testing-base-url/inApps/v1/notifications/test',
                                                     {},
                                                     None,
                                                     400)
        try:
            await client.request_test_notification()
        except APIException as e:
            self.assertEqual(400, e.http_status_code)
            self.assertEqual(9990000, e.raw_api_error)
            self.assertIsNone(e.api_error)
            self.assertEqual("Testing error.", e.error_message)
            return
        
        self.assertFalse(True)

    async def test_get_transaction_history_with_unknown_environment(self):
        client = self.get_client_with_body_from_file('tests/resources/models/transactionHistoryResponseWithMalformedEnvironment.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v2/history/1234', 
                                           {'revision': ['revision_input'],
                                            'startDate': ['123455'],
                                            'endDate': ['123456'],
                                            'productId': ['com.example.1', 'com.example.2'],
                                            'productType': ['CONSUMABLE', 'AUTO_RENEWABLE'],
                                            'sort': ['ASCENDING'],
                                            'subscriptionGroupIdentifier': ['sub_group_id', 'sub_group_id_2'],
                                            'inAppOwnershipType': ['FAMILY_SHARED'],
                                            'revoked': ['False']},
                                            None)

        request = TransactionHistoryRequest(
            sort=Order.ASCENDING,
            productTypes=[ProductType.CONSUMABLE, ProductType.AUTO_RENEWABLE],
            endDate=123456,
            startDate=123455,
            revoked=False,
            inAppOwnershipType=InAppOwnershipType.FAMILY_SHARED,
            productIds=['com.example.1', 'com.example.2'],
            subscriptionGroupIdentifiers=['sub_group_id', 'sub_group_id_2']
        )

        history_response = await client.get_transaction_history('1234', 'revision_input', request, GetTransactionHistoryVersion.V2)

        self.assertIsNone(history_response.environment)
        self.assertEqual("LocalTestingxxx", history_response.rawEnvironment)

    async def test_get_transaction_history_with_malformed_app_apple_id(self):
        client = self.get_client_with_body_from_file('tests/resources/models/transactionHistoryResponseWithMalformedAppAppleId.json',
                                           'GET',
                                           'https://local-testing-base-url/inApps/v1/history/1234', 
                                           {'revision': ['revision_input'],
                                            'startDate': ['123455'],
                                            'endDate': ['123456'],
                                            'productId': ['com.example.1', 'com.example.2'],
                                            'productType': ['CONSUMABLE', 'AUTO_RENEWABLE'],
                                            'sort': ['ASCENDING'],
                                            'subscriptionGroupIdentifier': ['sub_group_id', 'sub_group_id_2'],
                                            'inAppOwnershipType': ['FAMILY_SHARED'],
                                            'revoked': ['False']},
                                            None)

        request = TransactionHistoryRequest(
            sort=Order.ASCENDING,
            productTypes=[ProductType.CONSUMABLE, ProductType.AUTO_RENEWABLE],
            endDate=123456,
            startDate=123455,
            revoked=False,
            inAppOwnershipType=InAppOwnershipType.FAMILY_SHARED,
            productIds=['com.example.1', 'com.example.2'],
            subscriptionGroupIdentifiers=['sub_group_id', 'sub_group_id_2']
        )

        try:
            await client.get_transaction_history('1234', 'revision_input', request)
        except Exception:
            return
        
        self.assertFalse(True)

    def get_signing_key(self):
        return read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
    
    def get_client_with_body(self, body: str, expected_method: str, expected_url: str, expected_params: Dict[str, Union[str, List[str]]], expected_json: Dict[str, Any], status_code: int = 200):
        signing_key = self.get_signing_key()
        client = AsyncAppStoreServerAPIClient(signing_key, 'keyId', 'issuerId', 'com.example', Environment.LOCAL_TESTING)
        async def fake_execute_and_validate_inputs(method: bytes, url: str, params: Dict[str, Union[str, List[str]]], headers: Dict[str, str], json: Dict[str, Any]):
            self.assertEqual(expected_method, method)
            self.assertEqual(expected_url, url)
            self.assertEqual(expected_params, params)
            self.assertEqual(['User-Agent', 'Authorization', 'Accept'], list(headers.keys()))
            self.assertEqual('application/json', headers['Accept'])
            self.assertTrue(headers['User-Agent'].startswith('app-store-server-library/python'))
            self.assertTrue(headers['Authorization'].startswith('Bearer '))
            decoded_jwt = decode_json_from_signed_date(headers['Authorization'][7:])
            self.assertEqual('appstoreconnect-v1', decoded_jwt['payload']['aud'])
            self.assertEqual('issuerId', decoded_jwt['payload']['iss'])
            self.assertEqual('keyId', decoded_jwt['header']['kid'])
            self.assertEqual('com.example', decoded_jwt['payload']['bid'])
            self.assertEqual(expected_json, json)
            response = Response(status_code, headers={'Content-Type': 'application/json'}, content=body)
            return response

        client._execute_request = fake_execute_and_validate_inputs
        return client

    def get_client_with_body_from_file(self, path: str, expected_method: str, expected_url: str, expected_params: Dict[str, Union[str, List[str]]], expected_json: Dict[str, Any], status_code: int = 200):
        body = read_data_from_binary_file(path)
        return self.get_client_with_body(body, expected_method, expected_url, expected_params, expected_json, status_code)

