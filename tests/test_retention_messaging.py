# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

import inspect
import json
import unittest
import warnings
from uuid import UUID

from cattrs.errors import ClassValidationError

from appstoreserverlibrary.models.AlternateProduct import AlternateProduct
from appstoreserverlibrary.models.AdvancedCommerceInfo import AdvancedCommerceInfo
from appstoreserverlibrary.models.BillingPlanType import BillingPlanType
from appstoreserverlibrary.models.BulletPoint import BulletPoint
from appstoreserverlibrary.models.DecodedRealtimeRequestBody import DecodedRealtimeRequestBody
from appstoreserverlibrary.models.DefaultConfigurationRequest import DefaultConfigurationRequest
from appstoreserverlibrary.models.DefaultConfigurationResponse import DefaultConfigurationResponse
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.Message import Message
from appstoreserverlibrary.models.PerformanceTestConfig import PerformanceTestConfig
from appstoreserverlibrary.models.PerformanceTestResponse import PerformanceTestResponse
from appstoreserverlibrary.models.PerformanceTestResponseTimes import PerformanceTestResponseTimes
from appstoreserverlibrary.models.PerformanceTestResultResponse import PerformanceTestResultResponse
from appstoreserverlibrary.models.PerformanceTestStatus import PerformanceTestStatus
from appstoreserverlibrary.models.PromotionalOffer import PromotionalOffer
from appstoreserverlibrary.models.PromotionalOfferSignatureV1 import PromotionalOfferSignatureV1
from appstoreserverlibrary.models.RealtimeResponseBody import RealtimeResponseBody
from appstoreserverlibrary.models.RealtimeUrlRequest import RealtimeUrlRequest
from appstoreserverlibrary.models.RealtimeUrlResponse import RealtimeUrlResponse
from appstoreserverlibrary.models.SendAttemptResult import SendAttemptResult
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter
from tests.util import read_data_from_file


def performance_test_result_json(**kwargs) -> dict:
    values = json.loads(read_data_from_file('tests/resources/models/performanceTestResultResponse.json'))
    values.update(kwargs)
    return values


def create_performance_test_result_response(**kwargs) -> PerformanceTestResultResponse:
    values = dict(
        config=PerformanceTestConfig(maxConcurrentRequests=10, totalRequests=100, totalDuration=60000, responseTimeThreshold=500, successRateThreshold=95),
        target='https://example.com/retention',
        result=PerformanceTestStatus.PASS,
        successRate=98,
        numPending=0,
        responseTimes=PerformanceTestResponseTimes(average=120, p50=100, p90=200, p95=250, p99=400),
    )
    values.update(kwargs)
    return PerformanceTestResultResponse(**values)


class RetentionMessaging(unittest.TestCase):
    def test_realtime_response_body_with_message(self):
        # Create a RealtimeResponseBody with a Message
        message_id = UUID('a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890')
        message = Message(messageIdentifier=message_id)
        response_body = RealtimeResponseBody(message=message)

        # Serialize to dict
        c = _get_cattrs_converter(RealtimeResponseBody)
        json_dict = c.unstructure(response_body)

        # Validate structure
        self.assertIn('message', json_dict)
        self.assertIn('messageIdentifier', json_dict['message'])
        self.assertEqual('a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890', json_dict['message']['messageIdentifier'])
        self.assertNotIn('alternateProduct', json_dict)
        self.assertNotIn('promotionalOffer', json_dict)

        # Deserialize back
        deserialized = c.structure(json_dict, RealtimeResponseBody)

        # Verify
        self.assertIsNotNone(deserialized.message)
        self.assertEqual(message_id, deserialized.message.messageIdentifier)
        self.assertIsNone(deserialized.alternateProduct)
        self.assertIsNone(deserialized.promotionalOffer)

    def test_realtime_response_body_with_alternate_product(self):
        # Create a RealtimeResponseBody with an AlternateProduct
        message_id = UUID('b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901')
        product_id = 'com.example.alternate.product'
        alternate_product = AlternateProduct(messageIdentifier=message_id, productId=product_id, billingPlanType=BillingPlanType.MONTHLY)
        response_body = RealtimeResponseBody(alternateProduct=alternate_product)

        # Serialize to dict
        c = _get_cattrs_converter(RealtimeResponseBody)
        json_dict = c.unstructure(response_body)

        # Validate structure
        self.assertIn('alternateProduct', json_dict)
        self.assertIn('messageIdentifier', json_dict['alternateProduct'])
        self.assertIn('productId', json_dict['alternateProduct'])
        self.assertEqual('b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901', json_dict['alternateProduct']['messageIdentifier'])
        self.assertEqual('com.example.alternate.product', json_dict['alternateProduct']['productId'])
        self.assertEqual('MONTHLY', json_dict['alternateProduct']['billingPlanType'])
        self.assertNotIn('message', json_dict)
        self.assertNotIn('promotionalOffer', json_dict)

        # Deserialize back
        deserialized = c.structure(json_dict, RealtimeResponseBody)

        # Verify
        self.assertIsNone(deserialized.message)
        self.assertIsNotNone(deserialized.alternateProduct)
        self.assertEqual(message_id, deserialized.alternateProduct.messageIdentifier)
        self.assertEqual(product_id, deserialized.alternateProduct.productId)
        self.assertEqual(BillingPlanType.MONTHLY, deserialized.alternateProduct.billingPlanType)
        self.assertEqual("MONTHLY", deserialized.alternateProduct.rawBillingPlanType)
        self.assertIsNone(deserialized.promotionalOffer)

    def test_realtime_response_body_with_promotional_offer_v2(self):
        # Create a RealtimeResponseBody with a PromotionalOffer (V2 signature)
        message_id = UUID('c3d4e5f6-a789-0123-c3d4-e5f6a7890123')
        signature_v2 = 'signature2'
        promotional_offer = PromotionalOffer(messageIdentifier=message_id, promotionalOfferSignatureV2=signature_v2)
        response_body = RealtimeResponseBody(promotionalOffer=promotional_offer)

        # Serialize to dict
        c = _get_cattrs_converter(RealtimeResponseBody)
        json_dict = c.unstructure(response_body)

        # Validate structure
        self.assertIn('promotionalOffer', json_dict)
        self.assertIn('messageIdentifier', json_dict['promotionalOffer'])
        self.assertIn('promotionalOfferSignatureV2', json_dict['promotionalOffer'])
        self.assertEqual('c3d4e5f6-a789-0123-c3d4-e5f6a7890123', json_dict['promotionalOffer']['messageIdentifier'])
        self.assertEqual('signature2', json_dict['promotionalOffer']['promotionalOfferSignatureV2'])
        self.assertNotIn('promotionalOfferSignatureV1', json_dict['promotionalOffer'])
        self.assertNotIn('message', json_dict)
        self.assertNotIn('alternateProduct', json_dict)

        # Deserialize back
        deserialized = c.structure(json_dict, RealtimeResponseBody)

        # Verify
        self.assertIsNone(deserialized.message)
        self.assertIsNone(deserialized.alternateProduct)
        self.assertIsNotNone(deserialized.promotionalOffer)
        self.assertEqual(message_id, deserialized.promotionalOffer.messageIdentifier)
        self.assertEqual(signature_v2, deserialized.promotionalOffer.promotionalOfferSignatureV2)
        self.assertIsNone(deserialized.promotionalOffer.promotionalOfferSignatureV1)

    def test_realtime_response_body_with_promotional_offer_v1(self):
        # Create a RealtimeResponseBody with a PromotionalOffer (V1 signature)
        message_id = UUID('d4e5f6a7-8901-2345-d4e5-f6a789012345')
        nonce = UUID('e5f6a789-0123-4567-e5f6-a78901234567')
        app_account_token = UUID('f6a78901-2345-6789-f6a7-890123456789')
        signature_v1 = PromotionalOfferSignatureV1(
            encodedSignature='base64encodedSignature',
            productId='com.example.product',
            nonce=nonce,
            timestamp=1698148900000,
            keyId='keyId123',
            offerIdentifier='offer123',
            appAccountToken=app_account_token
        )

        promotional_offer = PromotionalOffer(messageIdentifier=message_id, promotionalOfferSignatureV1=signature_v1)
        response_body = RealtimeResponseBody(promotionalOffer=promotional_offer)

        # Serialize to dict
        c = _get_cattrs_converter(RealtimeResponseBody)
        json_dict = c.unstructure(response_body)

        # Validate structure
        self.assertIn('promotionalOffer', json_dict)
        self.assertIn('messageIdentifier', json_dict['promotionalOffer'])
        self.assertIn('promotionalOfferSignatureV1', json_dict['promotionalOffer'])
        self.assertEqual('d4e5f6a7-8901-2345-d4e5-f6a789012345', json_dict['promotionalOffer']['messageIdentifier'])

        v1_node = json_dict['promotionalOffer']['promotionalOfferSignatureV1']
        self.assertIn('encodedSignature', v1_node)
        self.assertIn('productId', v1_node)
        self.assertIn('nonce', v1_node)
        self.assertIn('timestamp', v1_node)
        self.assertIn('keyId', v1_node)
        self.assertIn('offerIdentifier', v1_node)
        self.assertIn('appAccountToken', v1_node)
        self.assertEqual('base64encodedSignature', v1_node['encodedSignature'])
        self.assertEqual('com.example.product', v1_node['productId'])
        self.assertEqual('e5f6a789-0123-4567-e5f6-a78901234567', v1_node['nonce'])
        self.assertEqual(1698148900000, v1_node['timestamp'])
        self.assertEqual('keyId123', v1_node['keyId'])
        self.assertEqual('offer123', v1_node['offerIdentifier'])
        self.assertEqual('f6a78901-2345-6789-f6a7-890123456789', v1_node['appAccountToken'])

        self.assertNotIn('promotionalOfferSignatureV2', json_dict['promotionalOffer'])
        self.assertNotIn('message', json_dict)
        self.assertNotIn('alternateProduct', json_dict)

        # Deserialize back
        deserialized = c.structure(json_dict, RealtimeResponseBody)

        # Verify
        self.assertIsNone(deserialized.message)
        self.assertIsNone(deserialized.alternateProduct)
        self.assertIsNotNone(deserialized.promotionalOffer)
        self.assertEqual(message_id, deserialized.promotionalOffer.messageIdentifier)
        self.assertIsNone(deserialized.promotionalOffer.promotionalOfferSignatureV2)
        self.assertIsNotNone(deserialized.promotionalOffer.promotionalOfferSignatureV1)

        deserialized_v1 = deserialized.promotionalOffer.promotionalOfferSignatureV1
        self.assertEqual('com.example.product', deserialized_v1.productId)
        self.assertEqual('offer123', deserialized_v1.offerIdentifier)
        self.assertEqual(nonce, deserialized_v1.nonce)
        self.assertEqual(1698148900000, deserialized_v1.timestamp)
        self.assertEqual('keyId123', deserialized_v1.keyId)
        self.assertEqual(app_account_token, deserialized_v1.appAccountToken)
        self.assertEqual('base64encodedSignature', deserialized_v1.encodedSignature)

    def test_realtime_response_body_with_advanced_commerce_info(self):
        message_id = UUID('a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890')
        ac_data = 'eyJhbGciOiJFUzI1NiJ9.base64data'
        ac_info = AdvancedCommerceInfo(messageIdentifier=message_id, advancedCommerceData=ac_data)
        response_body = RealtimeResponseBody(advancedCommerceInfo=ac_info)

        c = _get_cattrs_converter(RealtimeResponseBody)
        json_dict = c.unstructure(response_body)

        self.assertIn('advancedCommerceInfo', json_dict)
        self.assertEqual('a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890', json_dict['advancedCommerceInfo']['messageIdentifier'])
        self.assertEqual(ac_data, json_dict['advancedCommerceInfo']['advancedCommerceData'])
        self.assertNotIn('message', json_dict)
        self.assertNotIn('alternateProduct', json_dict)
        self.assertNotIn('promotionalOffer', json_dict)

        deserialized = c.structure(json_dict, RealtimeResponseBody)

        self.assertIsNone(deserialized.message)
        self.assertIsNone(deserialized.alternateProduct)
        self.assertIsNone(deserialized.promotionalOffer)
        self.assertIsNotNone(deserialized.advancedCommerceInfo)
        self.assertEqual(message_id, deserialized.advancedCommerceInfo.messageIdentifier)
        self.assertEqual(ac_data, deserialized.advancedCommerceInfo.advancedCommerceData)

    def test_performance_test_result_response_with_empty_failures(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        deserialized = c.structure(performance_test_result_json(failures={}), PerformanceTestResultResponse)

        self.assertEqual({}, deserialized.failures)
        self.assertEqual({}, deserialized.rawFailures)
        self.assertEqual({}, c.unstructure(deserialized)['failures'])

    def test_performance_test_result_response_with_only_unknown_failures(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        deserialized = c.structure(performance_test_result_json(failures={'NEW_REASON': 2}), PerformanceTestResultResponse)

        self.assertEqual({}, deserialized.failures)
        self.assertEqual({'NEW_REASON': 2}, deserialized.rawFailures)
        self.assertEqual({'NEW_REASON': 2}, c.unstructure(deserialized)['failures'])

    def test_performance_test_result_response_with_known_and_unknown_failures(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        deserialized = c.structure(performance_test_result_json(failures={'TIMED_OUT': 1, 'NEW_REASON': 2}), PerformanceTestResultResponse)

        self.assertEqual({SendAttemptResult.TIMED_OUT: 1}, deserialized.failures)
        self.assertEqual({'TIMED_OUT': 1, 'NEW_REASON': 2}, deserialized.rawFailures)

    def test_performance_test_result_response_round_trip(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        response_json = performance_test_result_json()

        deserialized = c.structure(response_json, PerformanceTestResultResponse)

        self.assertEqual(PerformanceTestStatus.PASS, deserialized.result)
        self.assertEqual('PASS', deserialized.rawResult)
        self.assertEqual(response_json, c.unstructure(deserialized))

    def test_performance_test_result_response_with_unknown_result(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        deserialized = c.structure(performance_test_result_json(result='NEW_RESULT'), PerformanceTestResultResponse)

        self.assertIsNone(deserialized.result)
        self.assertEqual('NEW_RESULT', deserialized.rawResult)

    def test_performance_test_result_response_without_required_field_fails_decoding(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        for field in ['config', 'target', 'successRate', 'numPending', 'responseTimes', 'result', 'failures']:
            response_json = performance_test_result_json()
            del response_json[field]
            with self.subTest(field=field), self.assertRaises(ClassValidationError):
                c.structure(response_json, PerformanceTestResultResponse)

    def test_performance_test_result_response_with_null_required_field_fails_decoding(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        for field in ['config', 'target', 'successRate', 'numPending', 'responseTimes', 'result', 'failures']:
            with self.subTest(field=field), self.assertRaises(ClassValidationError):
                c.structure(performance_test_result_json(**{field: None}), PerformanceTestResultResponse)

    def test_performance_test_result_response_without_nested_required_field_fails_decoding(self):
        c = _get_cattrs_converter(PerformanceTestResultResponse)
        response_json = performance_test_result_json()
        del response_json['config']['totalRequests']
        with self.assertRaises(ClassValidationError):
            c.structure(response_json, PerformanceTestResultResponse)

        response_json = performance_test_result_json()
        del response_json['responseTimes']['p99']
        with self.assertRaises(ClassValidationError):
            c.structure(response_json, PerformanceTestResultResponse)

    def test_performance_test_result_response_requires_documented_fields(self):
        with self.assertRaises(TypeError):
            PerformanceTestResultResponse(target='https://example.com/retention', result=PerformanceTestStatus.PASS, successRate=98, numPending=0,
                                          responseTimes=PerformanceTestResponseTimes(average=120, p50=100, p90=200, p95=250, p99=400), failures={})
        with self.assertRaises(ValueError) as context:
            create_performance_test_result_response(result=None, failures={})
        self.assertEqual('Either result or rawResult must be provided', str(context.exception))
        with self.assertRaises(ValueError) as context:
            create_performance_test_result_response()
        self.assertEqual('Either failures or rawFailures must be provided', str(context.exception))

    def test_performance_test_result_response_takes_keyword_arguments_only(self):
        parameters = inspect.signature(PerformanceTestResultResponse).parameters
        self.assertEqual([], [name for name, p in parameters.items() if p.kind != inspect.Parameter.KEYWORD_ONLY])

        values = dict(
            config=PerformanceTestConfig(maxConcurrentRequests=10, totalRequests=100, totalDuration=60000, responseTimeThreshold=500, successRateThreshold=95),
            target='https://example.com/retention',
            result=PerformanceTestStatus.PASS,
            successRate=98,
            numPending=0,
            responseTimes=PerformanceTestResponseTimes(average=120, p50=100, p90=200, p95=250, p99=400),
            failures={SendAttemptResult.TIMED_OUT: 2},
        )
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            PerformanceTestResultResponse(*values.values())
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            PerformanceTestResultResponse(*[v for k, v in values.items() if k != 'result'], result=values['result'])
        with self.assertRaisesRegex(TypeError, 'positional argument'):
            PerformanceTestResultResponse(values['config'], **{k: v for k, v in values.items() if k != 'config'})

        response = PerformanceTestResultResponse(**values)

        for name, value in values.items():
            self.assertEqual(value, getattr(response, name))
        self.assertEqual('PASS', response.rawResult)
        self.assertEqual({'TIMED_OUT': 2}, response.rawFailures)
        response = create_performance_test_result_response(result=None, rawResult='NEW_STATUS', rawFailures={'NEW_REASON': 1})
        self.assertEqual('NEW_STATUS', response.rawResult)
        self.assertEqual({}, response.failures)

    def test_performance_test_result_response_failures_assignment(self):
        response = create_performance_test_result_response(failures={SendAttemptResult.TIMED_OUT: 2})
        self.assertEqual({'TIMED_OUT': 2}, response.rawFailures)

        response.failures = {}
        self.assertEqual({}, response.rawFailures)

        response.rawFailures = {'NO_RESPONSE': 3, 'NEW_REASON': 4}
        self.assertEqual({SendAttemptResult.NO_RESPONSE: 3}, response.failures)

        with self.assertRaises(ValueError):
            response.rawFailures = None
        with self.assertRaises(ValueError):
            response.failures = None
        self.assertEqual({SendAttemptResult.NO_RESPONSE: 3}, response.failures)
        self.assertEqual({'NO_RESPONSE': 3, 'NEW_REASON': 4}, response.rawFailures)

    def test_performance_test_result_response_accepts_raw_failures(self):
        response = create_performance_test_result_response(rawFailures={'TIMED_OUT': 1, 'NEW_REASON': 2})

        self.assertEqual({SendAttemptResult.TIMED_OUT: 1}, response.failures)
        self.assertEqual({'TIMED_OUT': 1, 'NEW_REASON': 2}, response.rawFailures)

    def test_performance_test_response_request_id_is_uuid(self):
        c = _get_cattrs_converter(PerformanceTestResponse)
        response_json = json.loads(read_data_from_file('tests/resources/models/performanceTestResponse.json'))
        response_json['requestId'] = 'C4B87A1D-2E3F-4A5B-9C6D-7E8F9A0B1C2D'

        response = c.structure(response_json, PerformanceTestResponse)

        self.assertEqual(UUID('c4b87a1d-2e3f-4a5b-9c6d-7e8f9a0b1c2d'), response.requestId)
        self.assertEqual('c4b87a1d-2e3f-4a5b-9c6d-7e8f9a0b1c2d', c.unstructure(response)['requestId'])

    def test_performance_test_response_without_required_field_fails_decoding(self):
        c = _get_cattrs_converter(PerformanceTestResponse)
        for field in ['config', 'requestId']:
            response_json = json.loads(read_data_from_file('tests/resources/models/performanceTestResponse.json'))
            del response_json[field]
            with self.subTest(field=field), self.assertRaises(ClassValidationError):
                c.structure(response_json, PerformanceTestResponse)

    def test_performance_test_response_with_null_required_field_fails_decoding(self):
        c = _get_cattrs_converter(PerformanceTestResponse)
        for field in ['config', 'requestId']:
            response_json = json.loads(read_data_from_file('tests/resources/models/performanceTestResponse.json'))
            response_json[field] = None
            with self.subTest(field=field), self.assertRaises(ClassValidationError):
                c.structure(response_json, PerformanceTestResponse)

    def test_realtime_url_response(self):
        c = _get_cattrs_converter(RealtimeUrlResponse)
        deserialized = c.structure({'realtimeURL': 'https://example.com/realtime'}, RealtimeUrlResponse)
        self.assertEqual('https://example.com/realtime', deserialized.realtimeURL)

    def test_realtime_url_response_without_realtime_url_fails(self):
        c = _get_cattrs_converter(RealtimeUrlResponse)
        with self.assertRaises(ClassValidationError):
            c.structure({}, RealtimeUrlResponse)
        with self.assertRaises(TypeError):
            RealtimeUrlResponse()

    def test_realtime_url_response_with_null_realtime_url_fails(self):
        c = _get_cattrs_converter(RealtimeUrlResponse)
        with self.assertRaises(ClassValidationError):
            c.structure({'realtimeURL': None}, RealtimeUrlResponse)
        with self.assertRaises(ValueError):
            RealtimeUrlResponse(realtimeURL=None)

    def test_default_configuration_response_requires_message_identifier(self):
        c = _get_cattrs_converter(DefaultConfigurationResponse)
        response = c.structure({'messageIdentifier': 'A1B2C3D4-E5F6-7890-A1B2-C3D4E5F67890'}, DefaultConfigurationResponse)
        self.assertEqual(UUID('a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890'), response.messageIdentifier)
        with self.assertRaises(ClassValidationError):
            c.structure({'messageIdentifier': None}, DefaultConfigurationResponse)
        with self.assertRaises(ClassValidationError):
            c.structure({}, DefaultConfigurationResponse)

    def test_retention_messaging_required_fields_reject_none_when_built(self):
        with self.assertRaises(ValueError) as context:
            AlternateProduct(messageIdentifier=UUID('b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901'), productId=None)
        self.assertEqual('productId cannot be None', str(context.exception))
        with self.assertRaises(ValueError) as context:
            DefaultConfigurationRequest(messageIdentifier=None)
        self.assertEqual('messageIdentifier cannot be None', str(context.exception))
        with self.assertRaises(ValueError) as context:
            RealtimeUrlRequest(realtimeURL=None)
        self.assertEqual('realtimeURL cannot be None', str(context.exception))
        with self.assertRaises(ValueError) as context:
            BulletPoint(text=None, imageIdentifier=UUID('c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012'), altText='Bullet alt')
        self.assertEqual('text cannot be None', str(context.exception))
        with self.assertRaises(ValueError):
            BulletPoint(text='a' * 67, imageIdentifier=UUID('c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012'), altText='Bullet alt')

        bullet_point = BulletPoint(text='Bullet 1', imageIdentifier=UUID('c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012'), altText='Bullet alt')
        with self.assertRaises(ValueError):
            bullet_point.imageIdentifier = None
        self.assertEqual(UUID('c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012'), bullet_point.imageIdentifier)

    def test_default_configuration_request_with_message_identifier(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            request = DefaultConfigurationRequest(messageIdentifier=UUID('a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890'))
        self.assertEqual([], [w for w in caught if issubclass(w.category, DeprecationWarning)])

        c = _get_cattrs_converter(DefaultConfigurationRequest)
        self.assertEqual({'messageIdentifier': 'a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890'}, c.unstructure(request))

    def test_default_configuration_request_requires_message_identifier(self):
        with self.assertRaises(TypeError):
            DefaultConfigurationRequest()

    def test_alternate_product_requires_documented_fields(self):
        with self.assertRaises(TypeError):
            AlternateProduct(productId='com.example.alternate.product')
        with self.assertRaises(TypeError):
            AlternateProduct(messageIdentifier=UUID('b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901'))

        alternate_product = AlternateProduct(messageIdentifier=UUID('b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901'), productId='com.example.alternate.product')
        self.assertEqual({'messageIdentifier': 'b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901', 'productId': 'com.example.alternate.product'},
                         _get_cattrs_converter(AlternateProduct).unstructure(alternate_product))
