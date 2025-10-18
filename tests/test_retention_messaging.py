# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

import unittest
from uuid import UUID

from appstoreserverlibrary.models.AlternateProduct import AlternateProduct
from appstoreserverlibrary.models.DecodedRealtimeRequestBody import DecodedRealtimeRequestBody
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.Message import Message
from appstoreserverlibrary.models.PromotionalOffer import PromotionalOffer
from appstoreserverlibrary.models.PromotionalOfferSignatureV1 import PromotionalOfferSignatureV1
from appstoreserverlibrary.models.RealtimeResponseBody import RealtimeResponseBody
from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter


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
        alternate_product = AlternateProduct(messageIdentifier=message_id, productId=product_id)
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
        self.assertNotIn('message', json_dict)
        self.assertNotIn('promotionalOffer', json_dict)

        # Deserialize back
        deserialized = c.structure(json_dict, RealtimeResponseBody)

        # Verify
        self.assertIsNone(deserialized.message)
        self.assertIsNotNone(deserialized.alternateProduct)
        self.assertEqual(message_id, deserialized.alternateProduct.messageIdentifier)
        self.assertEqual(product_id, deserialized.alternateProduct.productId)
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
