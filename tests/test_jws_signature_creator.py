# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

from attr import define
import attr
import base64
import json
import jwt
import unittest
from appstoreserverlibrary.jws_signature_creator import AdvancedCommerceAPIInAppRequest, AdvancedCommerceAPIInAppSignatureCreator, IntroductoryOfferEligibilitySignatureCreator, PromotionalOfferV2SignatureCreator
from tests.util import read_data_from_binary_file

@define
class TestInAppRequest(AdvancedCommerceAPIInAppRequest):
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
        signature_creator = AdvancedCommerceAPIInAppSignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
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
        signature_creator = AdvancedCommerceAPIInAppSignatureCreator(signing_key, 'keyId', 'issuerId', 'bundleId')
        with self.assertRaises(ValueError):
            signature_creator.create_signature(None)