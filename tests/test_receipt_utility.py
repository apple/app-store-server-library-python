# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
from appstoreserverlibrary.receipt_utility import ReceiptUtility

from tests.util import read_data_from_file

APP_RECEIPT_EXPECTED_TRANSACTION_ID = "0"
TRANSACTION_RECEIPT_EXPECTED_TRANSACTION_ID = "33993399"

class ReceiptUtilityTest(unittest.TestCase):
    def test_xcode_app_receipt_extraction_with_no_transactions(self):
        receipt = read_data_from_file("tests/resources/xcode/xcode-app-receipt-empty")

        receipt_util = ReceiptUtility()

        extracted_transaction_id = receipt_util.extract_transaction_id_from_app_receipt(receipt)

        self.assertIsNone(extracted_transaction_id)

    def test_xcode_app_receipt_extraction_with_transactions(self):
        receipt = read_data_from_file("tests/resources/xcode/xcode-app-receipt-with-transaction")

        receipt_util = ReceiptUtility()

        extracted_transaction_id = receipt_util.extract_transaction_id_from_app_receipt(receipt)

        self.assertEqual(APP_RECEIPT_EXPECTED_TRANSACTION_ID, extracted_transaction_id)

    def test_transaction_receipt_extraction(self):
        receipt = read_data_from_file("tests/resources/mock_signed_data/legacyTransaction")

        receipt_util = ReceiptUtility()

        extracted_transaction_id = receipt_util.extract_transaction_id_from_transaction_receipt(receipt)

        self.assertEqual(TRANSACTION_RECEIPT_EXPECTED_TRANSACTION_ID, extracted_transaction_id)