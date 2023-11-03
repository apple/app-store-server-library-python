# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
from appstoreserverlibrary.promotional_offer import PromotionalOfferSignatureCreator

from tests.util import read_data_from_binary_file
from uuid import UUID


class PromotionalOfferSignatureCreatorTest(unittest.TestCase):
    def test_signature_creator(self):
        signing_key = read_data_from_binary_file('tests/resources/certs/testSigningKey.p8')
        signature_creator = PromotionalOfferSignatureCreator(signing_key, 'keyId', 'bundleId')
        signature = signature_creator.create_signature("productId", "offerId", "applicationUsername", UUID("20fba8a0-2b80-4a7d-a17f-85c1854727f8"), 1698148900000)
        self.assertIsNotNone(signature)