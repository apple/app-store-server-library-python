# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from abc import ABC
import importlib
import inspect
import json
import pkgutil
from typing import Optional, Union, get_args, get_origin
import unittest
from uuid import UUID

import attr
from cattrs.errors import ClassValidationError
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from appstoreserverlibrary.models.AccountTenure import AccountTenure
from appstoreserverlibrary.models.ConsumptionRequest import ConsumptionRequest
from appstoreserverlibrary.models.ConsumptionRequestV1 import ConsumptionRequestV1
from appstoreserverlibrary.models.ConsumptionStatus import ConsumptionStatus
from appstoreserverlibrary.models.DeliveryStatus import DeliveryStatus
from appstoreserverlibrary.models.DeliveryStatusV1 import DeliveryStatusV1
from appstoreserverlibrary.models.ExtendReasonCode import ExtendReasonCode
from appstoreserverlibrary.models.ExtendRenewalDateRequest import ExtendRenewalDateRequest
from appstoreserverlibrary.models.JWSTransactionDecodedPayload import JWSTransactionDecodedPayload
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter, metadata_required_key, metadata_type_key
from appstoreserverlibrary.models.LifetimeDollarsPurchased import LifetimeDollarsPurchased
from appstoreserverlibrary.models.LifetimeDollarsRefunded import LifetimeDollarsRefunded
from appstoreserverlibrary.models.MassExtendRenewalDateRequest import MassExtendRenewalDateRequest
from appstoreserverlibrary.models.MassExtendRenewalDateResponse import MassExtendRenewalDateResponse
from appstoreserverlibrary.models.MassExtendRenewalDateStatusResponse import MassExtendRenewalDateStatusResponse
from appstoreserverlibrary.models.NotificationHistoryRequest import NotificationHistoryRequest
from appstoreserverlibrary.models.NotificationTypeV2 import NotificationTypeV2
from appstoreserverlibrary.models.Platform import Platform
from appstoreserverlibrary.models.PlayTime import PlayTime
from appstoreserverlibrary.models.RealtimeUrlResponse import RealtimeUrlResponse
from appstoreserverlibrary.models.RefundPreferenceV1 import RefundPreferenceV1
from appstoreserverlibrary.models.Subtype import Subtype
from appstoreserverlibrary.models.Summary import Summary
from appstoreserverlibrary.models.TransactionCommitmentInfo import TransactionCommitmentInfo
from appstoreserverlibrary.models.TransactionHistoryRequest import Order, ProductType
from appstoreserverlibrary.models.UpdateAppAccountTokenRequest import UpdateAppAccountTokenRequest
from appstoreserverlibrary.models.UserStatus import UserStatus

import appstoreserverlibrary.models
from appstoreserverlibrary.signed_data_verifier import VerificationException, VerificationStatus
from tests.util import get_default_signed_data_verifier, read_data_from_file


def create_consumption_request_v1(**kwargs) -> ConsumptionRequestV1:
    values = dict(
        customerConsented=True,
        consumptionStatus=ConsumptionStatus.NOT_CONSUMED,
        platform=Platform.NON_APPLE,
        sampleContentProvided=False,
        deliveryStatus=DeliveryStatusV1.DID_NOT_DELIVER_DUE_TO_SERVER_OUTAGE,
        appAccountToken=UUID('7389a31a-fb6d-4569-a2a6-db7d85d84813'),
        accountTenure=AccountTenure.THIRTY_DAYS_TO_NINETY_DAYS,
        playTime=PlayTime.ONE_DAY_TO_FOUR_DAYS,
        lifetimeDollarsRefunded=LifetimeDollarsRefunded.ONE_HUNDRED_DOLLARS_TO_FOUR_HUNDRED_NINETY_NINE_DOLLARS_AND_NINETY_NINE_CENTS,
        lifetimeDollarsPurchased=LifetimeDollarsPurchased.ONE_THOUSAND_DOLLARS_TO_ONE_THOUSAND_NINE_HUNDRED_NINETY_NINE_DOLLARS_AND_NINETY_NINE_CENTS,
        userStatus=UserStatus.LIMITED_ACCESS,
    )
    values.update(kwargs)
    return ConsumptionRequestV1(**values)


EXTEND_RENEWAL_DATE_REQUESTS = [
    (ExtendRenewalDateRequest, dict(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac')),
    (MassExtendRenewalDateRequest, dict(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac', productId='com.example.productId')),
]


class APIModels(unittest.TestCase):
    def test_consumption_request_v1_sends_empty_app_account_token_when_none(self):
        consumption_request = create_consumption_request_v1(appAccountToken=None)

        json_dict = _get_cattrs_converter(ConsumptionRequestV1).unstructure(consumption_request)

        self.assertIsNone(consumption_request.appAccountToken)
        self.assertEqual('', json_dict['appAccountToken'])

    def test_consumption_request_v1_sends_empty_app_account_token_when_set_to_none(self):
        consumption_request = create_consumption_request_v1(appAccountToken=UUID('7389a31a-fb6d-4569-a2a6-db7d85d84813'))
        consumption_request.appAccountToken = None

        json_dict = _get_cattrs_converter(ConsumptionRequestV1).unstructure(consumption_request)

        self.assertEqual('', json_dict['appAccountToken'])

    def test_consumption_request_v1_sends_provided_app_account_token(self):
        consumption_request = create_consumption_request_v1(appAccountToken=UUID('7389A31A-FB6D-4569-A2A6-DB7D85D84813'))

        json_dict = _get_cattrs_converter(ConsumptionRequestV1).unstructure(consumption_request)

        self.assertEqual(UUID('7389a31a-fb6d-4569-a2a6-db7d85d84813'), consumption_request.appAccountToken)
        self.assertEqual('7389a31a-fb6d-4569-a2a6-db7d85d84813', json_dict['appAccountToken'])

    def test_consumption_request_v1_takes_keyword_arguments_only(self):
        parameters = inspect.signature(ConsumptionRequestV1).parameters
        self.assertEqual([], [name for name, p in parameters.items() if p.kind != inspect.Parameter.KEYWORD_ONLY])

        values = dict(
            customerConsented=True,
            consumptionStatus=ConsumptionStatus.NOT_CONSUMED,
            platform=Platform.NON_APPLE,
            sampleContentProvided=False,
            deliveryStatus=DeliveryStatusV1.DID_NOT_DELIVER_DUE_TO_SERVER_OUTAGE,
            appAccountToken=UUID('7389a31a-fb6d-4569-a2a6-db7d85d84813'),
            accountTenure=AccountTenure.THIRTY_DAYS_TO_NINETY_DAYS,
            playTime=PlayTime.ONE_DAY_TO_FOUR_DAYS,
            lifetimeDollarsRefunded=LifetimeDollarsRefunded.ONE_HUNDRED_DOLLARS_TO_FOUR_HUNDRED_NINETY_NINE_DOLLARS_AND_NINETY_NINE_CENTS,
            lifetimeDollarsPurchased=LifetimeDollarsPurchased.ONE_THOUSAND_DOLLARS_TO_ONE_THOUSAND_NINE_HUNDRED_NINETY_NINE_DOLLARS_AND_NINETY_NINE_CENTS,
            userStatus=UserStatus.LIMITED_ACCESS,
            refundPreference=RefundPreferenceV1.NO_PREFERENCE,
        )
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            ConsumptionRequestV1(*values.values())
        enums = ['consumptionStatus', 'platform', 'deliveryStatus']
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            ConsumptionRequestV1(*[v for k, v in values.items() if k not in enums], **{k: values[k] for k in enums})
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            ConsumptionRequestV1(True, **{k: v for k, v in values.items() if k != 'customerConsented'})

        consumption_request = ConsumptionRequestV1(**values)

        for name, value in values.items():
            self.assertEqual(value, getattr(consumption_request, name))
        self.assertEqual(1, consumption_request.rawConsumptionStatus)
        self.assertEqual(2, consumption_request.rawPlatform)
        self.assertEqual(3, consumption_request.rawDeliveryStatus)
        self.assertEqual(3, consumption_request.rawRefundPreference)
        self.assertEqual(7, create_consumption_request_v1(platform=None, rawPlatform=7).rawPlatform)

    def test_update_app_account_token_request_sends_lowercase_uuid(self):
        request = UpdateAppAccountTokenRequest(appAccountToken=UUID('7389A31A-FB6D-4569-A2A6-DB7D85D84813'))

        self.assertEqual({'appAccountToken': '7389a31a-fb6d-4569-a2a6-db7d85d84813'},
                         _get_cattrs_converter(UpdateAppAccountTokenRequest).unstructure(request))
        with self.assertRaises(TypeError):
            UpdateAppAccountTokenRequest()

    def test_consumption_request_required_enum_set_to_none_error_names_field(self):
        consumption_request = ConsumptionRequest(customerConsented=True, sampleContentProvided=False, deliveryStatus=DeliveryStatus.DELIVERED)

        with self.assertRaises(ValueError) as context:
            consumption_request.deliveryStatus = None

        self.assertEqual('deliveryStatus cannot be set to None when field is required', str(context.exception))

    def test_consumption_request_v1_serializes_every_required_field(self):
        json_dict = _get_cattrs_converter(ConsumptionRequestV1).unstructure(create_consumption_request_v1())

        self.assertEqual({
            'customerConsented': True,
            'consumptionStatus': 1,
            'platform': 2,
            'sampleContentProvided': False,
            'deliveryStatus': 3,
            'appAccountToken': '7389a31a-fb6d-4569-a2a6-db7d85d84813',
            'accountTenure': 4,
            'playTime': 5,
            'lifetimeDollarsRefunded': 4,
            'lifetimeDollarsPurchased': 6,
            'userStatus': 4,
        }, json_dict)

    def test_consumption_request_v1_requires_documented_fields(self):
        for field in ['customerConsented', 'sampleContentProvided', 'appAccountToken']:
            values = dict(customerConsented=True, sampleContentProvided=False, appAccountToken=None)
            del values[field]
            with self.subTest(field=field), self.assertRaises(TypeError):
                ConsumptionRequestV1(consumptionStatus=ConsumptionStatus.NOT_CONSUMED, platform=Platform.NON_APPLE,
                                     deliveryStatus=DeliveryStatusV1.DELIVERED_AND_WORKING_PROPERLY,
                                     accountTenure=AccountTenure.UNDECLARED, playTime=PlayTime.UNDECLARED,
                                     lifetimeDollarsRefunded=LifetimeDollarsRefunded.UNDECLARED,
                                     lifetimeDollarsPurchased=LifetimeDollarsPurchased.UNDECLARED,
                                     userStatus=UserStatus.UNDECLARED, **values)

        for field in ['consumptionStatus', 'platform', 'deliveryStatus', 'accountTenure', 'playTime', 'lifetimeDollarsRefunded', 'lifetimeDollarsPurchased', 'userStatus']:
            with self.subTest(field=field), self.assertRaises(ValueError) as context:
                create_consumption_request_v1(**{field: None})
            self.assertEqual(f'Either {field} or raw{field[0].upper() + field[1:]} must be provided', str(context.exception))

    def test_consumption_request_v1_accepts_raw_values_for_required_enums(self):
        consumption_request = create_consumption_request_v1(platform=None, rawPlatform=7)

        self.assertIsNone(consumption_request.platform)
        self.assertEqual(7, consumption_request.rawPlatform)
        self.assertEqual(7, _get_cattrs_converter(ConsumptionRequestV1).unstructure(consumption_request)['platform'])

    def test_consumption_request_requires_documented_fields(self):
        with self.assertRaises(TypeError):
            ConsumptionRequest(sampleContentProvided=False, deliveryStatus=DeliveryStatus.DELIVERED)
        with self.assertRaises(TypeError):
            ConsumptionRequest(customerConsented=True, deliveryStatus=DeliveryStatus.DELIVERED)
        with self.assertRaises(ValueError):
            ConsumptionRequest(customerConsented=True, sampleContentProvided=False)

    def test_extend_renewal_date_request_requires_documented_fields(self):
        request = ExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac')
        self.assertEqual({'extendByDays': 45, 'extendReasonCode': 1, 'requestIdentifier': 'fdf964a4-233b-486c-aac1-97d8d52688ac'},
                         _get_cattrs_converter(ExtendRenewalDateRequest).unstructure(request))

        with self.assertRaises(TypeError):
            ExtendRenewalDateRequest(extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac')
        with self.assertRaises(TypeError):
            ExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION)
        with self.assertRaises(ValueError) as context:
            ExtendRenewalDateRequest(extendByDays=45, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac')
        self.assertEqual('Either extendReasonCode or rawExtendReasonCode must be provided', str(context.exception))

    def test_mass_extend_renewal_date_request_requires_documented_fields(self):
        request = MassExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac', productId='com.example.productId')
        self.assertEqual({'extendByDays': 45, 'extendReasonCode': 1, 'requestIdentifier': 'fdf964a4-233b-486c-aac1-97d8d52688ac', 'productId': 'com.example.productId'},
                         _get_cattrs_converter(MassExtendRenewalDateRequest).unstructure(request))

        with self.assertRaises(TypeError):
            MassExtendRenewalDateRequest(extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac', productId='com.example.productId')
        with self.assertRaises(TypeError):
            MassExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, productId='com.example.productId')
        with self.assertRaises(TypeError):
            MassExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac', storefrontCountryCodes=['USA'])
        with self.assertRaises(ValueError) as context:
            MassExtendRenewalDateRequest(extendByDays=45, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac', productId='com.example.productId')
        self.assertEqual('Either extendReasonCode or rawExtendReasonCode must be provided', str(context.exception))

    def test_extend_renewal_date_requests_take_keyword_arguments_only(self):
        for cls, values in EXTEND_RENEWAL_DATE_REQUESTS:
            with self.subTest(cls=cls.__name__):
                parameters = inspect.signature(cls).parameters
                self.assertEqual([], [name for name, p in parameters.items() if p.kind != inspect.Parameter.KEYWORD_ONLY])

                with self.assertRaisesRegex(TypeError, 'positional argument'):
                    cls(*values.values())
                with self.assertRaisesRegex(TypeError, 'positional argument'):
                    cls(45, **{k: v for k, v in values.items() if k != 'extendByDays'})

                request = cls(**values)
                for name, value in values.items():
                    self.assertEqual(value, getattr(request, name))

    def test_extend_renewal_date_requests_send_unknown_raw_extend_reason_code(self):
        for cls, values in EXTEND_RENEWAL_DATE_REQUESTS:
            values = {k: v for k, v in values.items() if k != 'extendReasonCode'}
            with self.subTest(cls=cls.__name__):
                request = cls(rawExtendReasonCode=99, **values)

                self.assertIsNone(request.extendReasonCode)
                self.assertEqual(99, request.rawExtendReasonCode)
                self.assertEqual(dict(values, extendReasonCode=99), _get_cattrs_converter(cls).unstructure(request))

                self.assertEqual(ExtendReasonCode.SERVICE_ISSUE_OR_OUTAGE, cls(rawExtendReasonCode=3, **values).extendReasonCode)

                request.rawExtendReasonCode = 100
                self.assertIsNone(request.extendReasonCode)
                self.assertEqual(100, _get_cattrs_converter(cls).unstructure(request)['extendReasonCode'])
                with self.assertRaises(ValueError):
                    request.rawExtendReasonCode = None
                self.assertEqual(100, request.rawExtendReasonCode)

    def test_extend_renewal_date_requests_send_typed_extend_reason_code(self):
        for cls, values in EXTEND_RENEWAL_DATE_REQUESTS:
            with self.subTest(cls=cls.__name__):
                request = cls(**values)

                self.assertEqual(ExtendReasonCode.CUSTOMER_SATISFACTION, request.extendReasonCode)
                self.assertEqual(1, request.rawExtendReasonCode)
                self.assertEqual(dict(values, extendReasonCode=1), _get_cattrs_converter(cls).unstructure(request))

                request.extendReasonCode = ExtendReasonCode.OTHER
                self.assertEqual(2, request.rawExtendReasonCode)
                self.assertEqual(2, _get_cattrs_converter(cls).unstructure(request)['extendReasonCode'])
                with self.assertRaises(ValueError):
                    request.extendReasonCode = None
                self.assertEqual(ExtendReasonCode.OTHER, request.extendReasonCode)

    def test_notification_history_request_requires_documented_fields(self):
        with self.assertRaises(TypeError):
            NotificationHistoryRequest(startDate=1698148900000)
        with self.assertRaises(TypeError):
            NotificationHistoryRequest(endDate=1698148950000)

    def test_notification_history_request_takes_keyword_arguments_only(self):
        parameters = inspect.signature(NotificationHistoryRequest).parameters
        self.assertEqual(['startDate', 'endDate', 'notificationType', 'rawNotificationType', 'notificationSubtype', 'rawNotificationSubtype', 'onlyFailures', 'transactionId'],
                         list(parameters))
        self.assertEqual([], [name for name, p in parameters.items() if p.kind != inspect.Parameter.KEYWORD_ONLY])
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            NotificationHistoryRequest(1698148900000, 1698148950000)

    def test_notification_history_request_sends_unknown_raw_notification_type_and_subtype(self):
        request = NotificationHistoryRequest(startDate=1698148900000, endDate=1698148950000, rawNotificationType='NEW_NOTIFICATION_TYPE', rawNotificationSubtype='NEW_SUBTYPE')

        self.assertIsNone(request.notificationType)
        self.assertEqual('NEW_NOTIFICATION_TYPE', request.rawNotificationType)
        self.assertIsNone(request.notificationSubtype)
        self.assertEqual('NEW_SUBTYPE', request.rawNotificationSubtype)
        self.assertEqual({'startDate': 1698148900000, 'endDate': 1698148950000, 'notificationType': 'NEW_NOTIFICATION_TYPE', 'notificationSubtype': 'NEW_SUBTYPE'},
                         _get_cattrs_converter(NotificationHistoryRequest).unstructure(request))

        request = NotificationHistoryRequest(startDate=1698148900000, endDate=1698148950000, rawNotificationType='SUBSCRIBED', rawNotificationSubtype='INITIAL_BUY')
        self.assertEqual(NotificationTypeV2.SUBSCRIBED, request.notificationType)
        self.assertEqual(Subtype.INITIAL_BUY, request.notificationSubtype)

        request.rawNotificationType = 'ANOTHER_NOTIFICATION_TYPE'
        request.rawNotificationSubtype = 'ANOTHER_SUBTYPE'
        self.assertIsNone(request.notificationType)
        self.assertIsNone(request.notificationSubtype)
        self.assertEqual({'startDate': 1698148900000, 'endDate': 1698148950000, 'notificationType': 'ANOTHER_NOTIFICATION_TYPE', 'notificationSubtype': 'ANOTHER_SUBTYPE'},
                         _get_cattrs_converter(NotificationHistoryRequest).unstructure(request))

    def test_notification_history_request_sends_typed_notification_type_and_subtype(self):
        request = NotificationHistoryRequest(startDate=1698148900000, endDate=1698148950000, notificationType=NotificationTypeV2.SUBSCRIBED, notificationSubtype=Subtype.INITIAL_BUY, transactionId='999733843', onlyFailures=True)

        self.assertEqual(NotificationTypeV2.SUBSCRIBED, request.notificationType)
        self.assertEqual('SUBSCRIBED', request.rawNotificationType)
        self.assertEqual(Subtype.INITIAL_BUY, request.notificationSubtype)
        self.assertEqual('INITIAL_BUY', request.rawNotificationSubtype)
        self.assertEqual('999733843', request.transactionId)
        self.assertTrue(request.onlyFailures)
        self.assertEqual({'startDate': 1698148900000, 'endDate': 1698148950000, 'notificationType': 'SUBSCRIBED', 'notificationSubtype': 'INITIAL_BUY', 'transactionId': '999733843', 'onlyFailures': True},
                         _get_cattrs_converter(NotificationHistoryRequest).unstructure(request))

        request.notificationType = None
        request.notificationSubtype = None
        self.assertIsNone(request.rawNotificationType)
        self.assertIsNone(request.rawNotificationSubtype)
        self.assertEqual({'startDate': 1698148900000, 'endDate': 1698148950000, 'transactionId': '999733843', 'onlyFailures': True},
                         _get_cattrs_converter(NotificationHistoryRequest).unstructure(request))

    def test_decoded_models_check_their_documented_limits(self):
        valid = [(TransactionCommitmentInfo, {'billingPeriodNumber': 1}), (TransactionCommitmentInfo, {'billingPeriodNumber': 12}),
                 (JWSTransactionDecodedPayload, {'revocationPercentage': 0}), (JWSTransactionDecodedPayload, {'revocationPercentage': 100000}),
                 (Summary, {'storefrontCountryCodes': ['USA']}),
                 (MassExtendRenewalDateResponse, {'requestIdentifier': 'a' * 128}),
                 (MassExtendRenewalDateStatusResponse, {'requestIdentifier': 'a' * 128}),
                 (RealtimeUrlResponse, {'realtimeURL': 'a' * 256})]
        invalid = [(TransactionCommitmentInfo, {'billingPeriodNumber': 0}), (TransactionCommitmentInfo, {'billingPeriodNumber': 13}),
                   (JWSTransactionDecodedPayload, {'revocationPercentage': -1}), (JWSTransactionDecodedPayload, {'revocationPercentage': 100001}),
                   (Summary, {'storefrontCountryCodes': ['USAA']}),
                   (MassExtendRenewalDateResponse, {'requestIdentifier': 'a' * 129}),
                   (MassExtendRenewalDateStatusResponse, {'requestIdentifier': 'a' * 129}),
                   (RealtimeUrlResponse, {'realtimeURL': 'a' * 257})]
        for model, value in valid:
            with self.subTest(model=model.__name__, value=value):
                decoded = _get_cattrs_converter(model).structure(value, model)
                key, expected = next(iter(value.items()))
                self.assertEqual(expected, getattr(decoded, key))
        for model, value in invalid:
            with self.subTest(model=model.__name__, value=value), self.assertRaises(ClassValidationError):
                _get_cattrs_converter(model).structure(value, model)

    def test_transaction_with_out_of_range_billing_period_number_fails_to_decode(self):
        transaction_json = json.loads(read_data_from_file('tests/resources/models/signedTransaction.json'))
        transaction_json['commitmentInfo']['billingPeriodNumber'] = 13
        private_key = ec.generate_private_key(ec.SECP256R1()).private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()).decode()
        signed_transaction = jwt.encode(payload=transaction_json, key=private_key, algorithm='ES256')

        with self.assertRaises(VerificationException) as context:
            get_default_signed_data_verifier().verify_and_decode_transaction(signed_transaction)
        self.assertEqual(VerificationStatus.VERIFICATION_FAILURE, context.exception.status)

    def test_transaction_history_request_enums(self):
        self.assertTrue('AUTO_RENEWABLE' in ProductType)
        self.assertFalse('INVALID' in ProductType)
        self.assertTrue('DESCENDING' in Order)
        self.assertFalse('INVALID' in Order)

    def test_required_fields_reject_none_when_built(self):
        cases = [
            (ExtendRenewalDateRequest, dict(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac')),
            (MassExtendRenewalDateRequest, dict(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='fdf964a4-233b-486c-aac1-97d8d52688ac', productId='com.example.productId')),
            (NotificationHistoryRequest, dict(startDate=1698148900000, endDate=1698148950000)),
            (UpdateAppAccountTokenRequest, dict(appAccountToken=UUID('7389a31a-fb6d-4569-a2a6-db7d85d84813'))),
            (ConsumptionRequest, dict(customerConsented=True, sampleContentProvided=False, deliveryStatus=DeliveryStatus.DELIVERED)),
        ]
        for cls, values in cases:
            for field in values:
                raw_backed = attr.fields_dict(cls)[field].metadata.get(metadata_type_key) == 'main'
                expected = f'Either {field} or raw{field[0].upper() + field[1:]} must be provided' if raw_backed else f'{field} cannot be None'
                with self.subTest(field=f'{cls.__name__}.{field}'):
                    with self.assertRaises(ValueError) as context:
                        cls(**dict(values, **{field: None}))
                    self.assertEqual(expected, str(context.exception))

                    model = cls(**values)
                    with self.assertRaises(ValueError):
                        setattr(model, field, None)
                    self.assertEqual(values[field], getattr(model, field))

        for field in ['customerConsented', 'sampleContentProvided']:
            with self.subTest(field=f'ConsumptionRequestV1.{field}'), self.assertRaises(ValueError):
                create_consumption_request_v1(**{field: None})

    def test_consumption_request_v1_app_account_token_is_mandatory_and_nullable(self):
        self.assertEqual(Optional[UUID], attr.fields(ConsumptionRequestV1).appAccountToken.type)
        self.assertIs(inspect.Parameter.empty, inspect.signature(ConsumptionRequestV1).parameters['appAccountToken'].default)
        consumption_request = create_consumption_request_v1(appAccountToken=None)
        self.assertIsNone(consumption_request.appAccountToken)

    def test_every_required_attribute_rejects_none(self):
        nullable = {'ConsumptionRequestV1.appAccountToken'}
        checked = 0
        for module_info in pkgutil.iter_modules(appstoreserverlibrary.models.__path__):
            module = importlib.import_module(f'appstoreserverlibrary.models.{module_info.name}')
            for cls in list(vars(module).values()):
                if not inspect.isclass(cls) or not attr.has(cls) or cls.__module__ != module.__name__ or ABC in cls.__bases__:
                    continue
                attr.resolve_types(cls)
                for attribute in attr.fields(cls):
                    if attribute.metadata.get(metadata_type_key) == 'raw':
                        required = attribute.metadata.get(metadata_required_key, False)
                    else:
                        required = attribute.init and attribute.default is attr.NOTHING
                    name = f'{cls.__name__}.{attribute.name}'
                    if not required or name in nullable:
                        continue
                    checked += 1
                    with self.subTest(attribute=name):
                        self.assertIsNotNone(attribute.validator)
                        with self.assertRaises(ValueError):
                            attribute.validator(None, attribute, None)
                        if not (get_origin(attribute.type) is Union and type(None) in get_args(attribute.type)):
                            with self.assertRaises(Exception):
                                _get_cattrs_converter(cls).structure(None, attribute.type)
        self.assertGreater(checked, 150)

    def test_every_model_takes_keyword_arguments_only(self):
        hand_written = {'AbstractAdvancedCommerceBaseItem', 'AbstractAdvancedCommerceInAppRequest', 'AbstractAdvancedCommerceItem',
                        'AbstractAdvancedCommerceResponse', 'AdvancedCommerceRequest', 'TransactionHistoryRequest'}
        positional_kinds = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.VAR_POSITIONAL)
        checked = 0
        for module_info in pkgutil.iter_modules(appstoreserverlibrary.models.__path__):
            module = importlib.import_module(f'appstoreserverlibrary.models.{module_info.name}')
            for name, cls in list(vars(module).items()):
                if not inspect.isclass(cls) or not attr.has(cls) or cls.__module__ != module.__name__ or name.startswith('_') \
                        or name in hand_written:
                    continue
                checked += 1
                with self.subTest(model=name):
                    parameters = inspect.signature(cls).parameters
                    self.assertEqual([], [p for p, parameter in parameters.items() if parameter.kind in positional_kinds])
        self.assertGreater(checked, 100)

    def test_extend_renewal_date_request_limits(self):
        for cls, extra in ((ExtendRenewalDateRequest, {}), (MassExtendRenewalDateRequest, {'productId': 'com.example.productId'})):
            with self.subTest(model=cls.__name__):
                for days in (1, 90):
                    request = cls(extendByDays=days, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='a' * 128, **extra)
                    self.assertEqual(days, request.extendByDays)
                    request.extendByDays = days
                    self.assertEqual(days, cls(extendByDays=days, rawExtendReasonCode=99, requestIdentifier='id', **extra).extendByDays)
                request = cls(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='id', **extra)
                for days in (0, 91):
                    with self.assertRaises(ValueError):
                        cls(extendByDays=days, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='id', **extra)
                    with self.assertRaises(ValueError):
                        cls(extendByDays=days, rawExtendReasonCode=99, requestIdentifier='id', **extra)
                    with self.assertRaises(ValueError):
                        request.extendByDays = days
                self.assertEqual(45, request.extendByDays)
                request.requestIdentifier = 'a' * 128
                with self.assertRaises(ValueError):
                    cls(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='a' * 129, **extra)
                with self.assertRaises(ValueError):
                    request.requestIdentifier = 'a' * 129
                self.assertEqual('a' * 128, request.requestIdentifier)

    def test_mass_extend_renewal_date_request_storefront_country_code_limits(self):
        request = MassExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='id',
                                               productId='com.example.productId', storefrontCountryCodes=['USA', 'CA'])
        self.assertEqual(['USA', 'CA'], request.storefrontCountryCodes)
        request.storefrontCountryCodes = None
        with self.assertRaises(ValueError):
            MassExtendRenewalDateRequest(extendByDays=45, extendReasonCode=ExtendReasonCode.CUSTOMER_SATISFACTION, requestIdentifier='id',
                                         productId='com.example.productId', storefrontCountryCodes=['USA', 'ABCD'])
        with self.assertRaises(ValueError):
            request.storefrontCountryCodes = ['ABCD']
        self.assertIsNone(request.storefrontCountryCodes)

    def test_consumption_request_consumption_percentage_limits(self):
        request = ConsumptionRequest(customerConsented=True, sampleContentProvided=False, deliveryStatus=DeliveryStatus.DELIVERED)
        self.assertIsNone(request.consumptionPercentage)
        for percentage in (0, 100000):
            self.assertEqual(percentage, ConsumptionRequest(customerConsented=True, sampleContentProvided=False, deliveryStatus=DeliveryStatus.DELIVERED,
                                                            consumptionPercentage=percentage).consumptionPercentage)
            request.consumptionPercentage = percentage
        for percentage in (-1, 100001):
            with self.assertRaises(ValueError):
                ConsumptionRequest(customerConsented=True, sampleContentProvided=False, deliveryStatus=DeliveryStatus.DELIVERED,
                                   consumptionPercentage=percentage)
            with self.assertRaises(ValueError):
                request.consumptionPercentage = percentage
        self.assertEqual(100000, request.consumptionPercentage)
        request.consumptionPercentage = None


if __name__ == '__main__':
    unittest.main()
