# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from attr import define
import attr
import base64
import json
import jwt
import unittest
from uuid import UUID
from cryptography.hazmat.primitives import serialization
from appstoreserverlibrary.jws_signature_creator import AdvancedCommerceInAppRequest, AdvancedCommerceInAppSignatureCreator, IntroductoryOfferEligibilitySignatureCreator, PromotionalOfferV2SignatureCreator
from appstoreserverlibrary.models.AdvancedCommerceEffective import AdvancedCommerceEffective
from appstoreserverlibrary.models.AdvancedCommerceRequestInfo import AdvancedCommerceRequestInfo
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyDescriptors import AdvancedCommerceSubscriptionModifyDescriptors
from appstoreserverlibrary.models.AdvancedCommerceSubscriptionModifyInAppRequest import AdvancedCommerceSubscriptionModifyInAppRequest
from tests.util import read_data_from_binary_file

@define
class TestInAppRequest(AdvancedCommerceInAppRequest):
    test_value: str

class JWSSignatureCreatorTest(unittest.TestCase):
    def test_promotional_offer_signature_creator(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferV2SignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        signature = signature_creator.create_signature("productId", "offerIdentifier", "transactionId")
        self.assertIsNotNone(signature)
        headers = jwt.get_unverified_header(signature)
        payload = jwt.decode(signature, options={"verify_signature": False})

        # Header
        self.assertEqual("JWT", headers["typ"])
        self.assertEqual("ES256", headers["alg"])
        self.assertEqual("keyId", headers["kid"])
        # Payload
        self.assertEqual("issuerId", payload['iss'])
        self.assertIsNotNone(payload['iat'])
        self.assertFalse('exp' in payload)
        self.assertEqual("promotional-offer", payload['aud'])
        self.assertEqual('bundleId', payload['bid'])
        self.assertIsNotNone(payload['nonce'])
        self.assertEqual('productId', payload['productId'])
        self.assertEqual('offerIdentifier', payload['offerIdentifier'])
        self.assertEqual('transactionId', payload['transactionId'])

    def test_promotional_offer_signature_creator_transaction_id_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferV2SignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        signature = signature_creator.create_signature("productId", "offerIdentifier", None)
        payload = jwt.decode(signature, options={"verify_signature": False})
        self.assertFalse('transactionId' in payload)

    def test_promotional_offer_signature_creator_transaction_id_omitted(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferV2SignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        signature = signature_creator.create_signature("productId", "offerIdentifier")
        payload = jwt.decode(signature, options={"verify_signature": False})
        self.assertEqual('productId', payload['productId'])
        self.assertEqual('offerIdentifier', payload['offerIdentifier'])
        self.assertFalse('transactionId' in payload)

    def test_promotional_offer_signature_creator_offer_identifier_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferV2SignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature("productId", None, "transactionId")

    def test_promotional_offer_signature_creator_product_id_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferV2SignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature(None, "offerIdentifier", "transactionId")
    
    def test_introductory_offer_eligibility_signature_creator(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = IntroductoryOfferEligibilitySignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        signature = signature_creator.create_signature("productId", True, "transactionId")
        self.assertIsNotNone(signature)
        headers = jwt.get_unverified_header(signature)
        payload = jwt.decode(signature, options={"verify_signature": False})

        # Header
        self.assertEqual("JWT", headers["typ"])
        self.assertEqual("ES256", headers["alg"])
        self.assertEqual("keyId", headers["kid"])
        # Payload
        self.assertEqual("issuerId", payload['iss'])
        self.assertIsNotNone(payload['iat'])
        self.assertFalse('exp' in payload)
        self.assertEqual("introductory-offer-eligibility", payload['aud'])
        self.assertEqual('bundleId', payload['bid'])
        self.assertIsNotNone(payload['nonce'])
        self.assertEqual('productId', payload['productId'])
        self.assertEqual(True, payload['allowIntroductoryOffer'])
        self.assertEqual('transactionId', payload['transactionId'])

    def test_introductory_offer_eligibility_signature_creator_transaction_id_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = IntroductoryOfferEligibilitySignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature("productId", True, None)
    
    def test_introductory_offer_eligibility_signature_creator_allow_introductory_offer_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = IntroductoryOfferEligibilitySignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature("productId", None, "transactionId")

    def test_introductory_offer_eligibility_signature_creator_product_id_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = IntroductoryOfferEligibilitySignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature(None, True, "transactionId")

    def test_advanced_commerce_api_in_app_signature_creator(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = AdvancedCommerceInAppSignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        request = TestInAppRequest("testValue")
        signature = signature_creator.create_signature(request)
        self.assertIsNotNone(signature)
        headers = jwt.get_unverified_header(signature)
        payload = jwt.decode(signature, options={"verify_signature": False})

        # Header
        self.assertEqual("JWT", headers["typ"])
        self.assertEqual("ES256", headers["alg"])
        self.assertEqual("keyId", headers["kid"])
        # Payload
        self.assertEqual("issuerId", payload['iss'])
        self.assertIsNotNone(payload['iat'])
        self.assertFalse('exp' in payload)
        self.assertEqual("advanced-commerce-api", payload['aud'])
        self.assertEqual('bundleId', payload['bid'])
        self.assertIsNotNone(payload['nonce'])
        request = payload['request']
        decode_json = json.loads(str(base64.b64decode(request).decode('utf-8')))
        self.assertEqual('testValue', decode_json['test_value'])

    def test_advanced_commerce_api_in_app_signature_creator_request_missing(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = AdvancedCommerceInAppSignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature(None)

    def test_advanced_commerce_in_app_signature_creator_with_subscription_modify_in_app_request(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = AdvancedCommerceInAppSignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        request = AdvancedCommerceSubscriptionModifyInAppRequest(
            requestInfo=AdvancedCommerceRequestInfo(requestReferenceId=UUID("550e8400-e29b-41d4-a716-446655440007")),
            transactionId="transactionId",
            retainBillingCycle=True,
            descriptors=AdvancedCommerceSubscriptionModifyDescriptors(effective=AdvancedCommerceEffective.IMMEDIATELY, description="description", displayName="display name"),
            taxCode="taxCode",
            currency="USD"
        )
        signature = signature_creator.create_signature(request)
        public_key = serialization.load_pem_private_key(signing_key, password=None).public_key()
        payload = jwt.decode(signature, public_key, algorithms=['ES256'], audience='advanced-commerce-api')
        self.assertEqual('advanced-commerce-api', payload['aud'])
        decode_json = json.loads(base64.b64decode(payload['request']).decode('utf-8'))
        self.assertEqual({
            "operation": "MODIFY_SUBSCRIPTION",
            "version": "1",
            "requestInfo": {
                "requestReferenceId": "550e8400-e29b-41d4-a716-446655440007"
            },
            "transactionId": "transactionId",
            "retainBillingCycle": True,
            "descriptors": {
                "effective": "IMMEDIATELY",
                "description": "description",
                "displayName": "display name"
            },
            "taxCode": "taxCode",
            "currency": "USD"
        }, decode_json)

    def test_advanced_commerce_in_app_requests_extend_advanced_commerce_in_app_request(self):
        self.assertTrue(issubclass(AdvancedCommerceSubscriptionModifyInAppRequest, AdvancedCommerceInAppRequest))
