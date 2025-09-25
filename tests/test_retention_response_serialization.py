# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
import json
from appstoreserverlibrary.models.RealtimeResponseBody import RealtimeResponseBody
from appstoreserverlibrary.models.Message import Message
from appstoreserverlibrary.models.AlternateProduct import AlternateProduct
from appstoreserverlibrary.models.PromotionalOffer import PromotionalOffer
from appstoreserverlibrary.models.PromotionalOfferSignatureV1 import PromotionalOfferSignatureV1

class RetentionResponseSerialization(unittest.TestCase):

    def test_message_response_serialization(self):
        response = RealtimeResponseBody(
            message=Message(messageIdentifier="msg123")
        )
        json_dict = response.to_json_dict()

        # Only message field should be present
        self.assertEqual(json_dict, {"message": {"messageIdentifier": "msg123"}})
        self.assertNotIn("alternateProduct", json_dict)
        self.assertNotIn("promotionalOffer", json_dict)

        # Verify JSON serialization works
        json_str = json.dumps(json_dict)
        self.assertEqual(json_str, '{"message": {"messageIdentifier": "msg123"}}')

    def test_alternate_product_response_serialization(self):
        response = RealtimeResponseBody(
            alternateProduct=AlternateProduct(
                messageIdentifier="msg456",
                productId="com.example.premium"
            )
        )
        json_dict = response.to_json_dict()

        expected = {
            "alternateProduct": {
                "messageIdentifier": "msg456",
                "productId": "com.example.premium"
            }
        }
        self.assertEqual(json_dict, expected)
        self.assertNotIn("message", json_dict)
        self.assertNotIn("promotionalOffer", json_dict)

    def test_promotional_offer_v2_response_serialization(self):
        response = RealtimeResponseBody(
            promotionalOffer=PromotionalOffer(
                messageIdentifier="msg789",
                promotionalOfferSignatureV2="eyJhbGciOiJFUzI1NiJ9.example.signature"
            )
        )
        json_dict = response.to_json_dict()

        expected = {
            "promotionalOffer": {
                "messageIdentifier": "msg789",
                "promotionalOfferSignatureV2": "eyJhbGciOiJFUzI1NiJ9.example.signature"
            }
        }
        self.assertEqual(json_dict, expected)
        self.assertNotIn("message", json_dict)
        self.assertNotIn("alternateProduct", json_dict)

    def test_promotional_offer_v1_response_serialization(self):
        v1_signature = PromotionalOfferSignatureV1(
            encodedSignature="base64signature==",
            productId="com.example.subscription",
            nonce="550e8400-e29b-41d4-a716-446655440000",
            offerId="intro_offer",
            timestamp=1681314324000,
            keyIdentifier="ABC123DEF4"
        )

        response = RealtimeResponseBody(
            promotionalOffer=PromotionalOffer(
                messageIdentifier="msg101112",
                promotionalOfferSignatureV1=v1_signature
            )
        )
        json_dict = response.to_json_dict()

        expected = {
            "promotionalOffer": {
                "messageIdentifier": "msg101112",
                "promotionalOfferSignatureV1": {
                    "encodedSignature": "base64signature==",
                    "productId": "com.example.subscription",
                    "nonce": "550e8400-e29b-41d4-a716-446655440000",
                    "offerId": "intro_offer",
                    "timestamp": 1681314324000,
                    "keyIdentifier": "ABC123DEF4"
                }
            }
        }
        self.assertEqual(json_dict, expected)

    def test_empty_response_serialization(self):
        response = RealtimeResponseBody()
        json_dict = response.to_json_dict()

        # Should be completely empty when no fields are set
        self.assertEqual(json_dict, {})

    def test_partial_fields_omitted(self):
        # Test that None fields in nested objects are omitted
        response = RealtimeResponseBody(
            message=Message()  # messageIdentifier is None
        )
        json_dict = response.to_json_dict()

        # Should include empty message object (this is correct behavior)
        self.assertEqual(json_dict, {"message": {}})

    def test_partial_nested_object_serialization(self):
        # Test nested object with only some fields populated
        v1_signature = PromotionalOfferSignatureV1(
            encodedSignature="signature123",
            productId="com.example.product"
            # Other fields are None and should be omitted
        )

        response = RealtimeResponseBody(
            promotionalOffer=PromotionalOffer(
                messageIdentifier="msgABC",
                promotionalOfferSignatureV1=v1_signature
                # promotionalOfferSignatureV2 is None and should be omitted
            )
        )
        json_dict = response.to_json_dict()

        expected = {
            "promotionalOffer": {
                "messageIdentifier": "msgABC",
                "promotionalOfferSignatureV1": {
                    "encodedSignature": "signature123",
                    "productId": "com.example.product"
                }
            }
        }
        self.assertEqual(json_dict, expected)

if __name__ == '__main__':
    unittest.main()