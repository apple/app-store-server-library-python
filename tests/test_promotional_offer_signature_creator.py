# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import base64
import unittest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import SHA256
from appstoreserverlibrary.promotional_offer import PromotionalOfferSignatureCreator

from tests.util import read_data_from_binary_file
from uuid import UUID


class PromotionalOfferSignatureCreatorTest(unittest.TestCase):
    def test_signature_creator(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferSignatureCreator(signing_key, 'keyId', 'bundleId')
        signature = signature_creator.create_signature("productId", "offerId", "appAccountToken", UUID("20fba8a0-2b80-4a7d-a17f-85c1854727f8"), 1698148900000)
        self.assertIsNotNone(signature)
        expected_payload = '\u2063'.join(['bundleId', 'keyId', 'productId', 'offerId', 'appaccounttoken', '20fba8a0-2b80-4a7d-a17f-85c1854727f8', '1698148900000'])
        public_key = serialization.load_pem_private_key(signing_key, password=None).public_key()
        public_key.verify(base64.b64decode(signature), expected_payload.encode('utf-8'), ECDSA(SHA256()))
