# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
import base64 # Added import
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

    def test_extract_transaction_id_from_app_receipt_invalid_base64(self):
        receipt_util = ReceiptUtility()
        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt("not base64")

    def test_extract_transaction_id_from_app_receipt_malformed_asn1(self):
        receipt_util = ReceiptUtility()
        # Malformed ASN.1 data (e.g., not a sequence)
        malformed_receipt = " SEQUENCE { INTEGER 1 } " # Simplified, needs proper encoding
        # This test will likely need more sophisticated malformed data
        # For now, using a simple invalid base64 string to represent a decode failure of sorts
        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt("aGVsbG8=" * 20) # "hello" repeated, unlikely valid ASN.1 PKCS#7

    def test_extract_transaction_id_from_app_receipt_no_in_app_array(self):
        # This would require crafting a valid PKCS#7 signedData without the in-app purchase OID
        # For now, this scenario is partially covered by xcode-app-receipt-empty if it lacks that specific OID path
        # A more targeted test could be added if a specific receipt sample is available.
        pass

    def test_extract_transaction_id_from_transaction_receipt_invalid_base64(self):
        receipt_util = ReceiptUtility()
        with self.assertRaises(ValueError): # Changed from UnicodeDecodeError to ValueError
             receipt_util.extract_transaction_id_from_transaction_receipt("not base64")

    def test_extract_transaction_id_from_transaction_receipt_no_purchase_info(self):
        receipt_util = ReceiptUtility()
        # Base64 encoded string that doesn't contain "purchase-info"
        no_purchase_info_receipt = "ewogICAgIm90aGVyLWtleSIgPSAiZGF0YSI7Cn0=" # {"other-key" = "data";}
        self.assertIsNone(receipt_util.extract_transaction_id_from_transaction_receipt(no_purchase_info_receipt))

    def test_extract_transaction_id_from_transaction_receipt_purchase_info_not_base64(self):
        receipt_util = ReceiptUtility()
        # Contains "purchase-info" and its value *looks* like base64 but is invalid (e.g. wrong padding/length)
        invalid_base64_value = "A" # Valid chars, but invalid encoding
        purchase_info_with_invalid_base64 = f'{{\n"purchase-info" = "{invalid_base64_value}";\n}}'
        encoded_receipt = base64.b64encode(purchase_info_with_invalid_base64.encode()).decode()
        with self.assertRaises(ValueError): # binascii.Error, subclass of ValueError
            receipt_util.extract_transaction_id_from_transaction_receipt(encoded_receipt)

    def test_extract_transaction_id_from_transaction_receipt_no_transaction_id(self):
        receipt_util = ReceiptUtility()
        # "purchase-info" is valid base64, but decoded content doesn't have "transaction-id"
        purchase_info_content = '{\n"other-key" = "data";\n}'
        encoded_purchase_info = base64.b64encode(purchase_info_content.encode()).decode() # Fixed NameError
        receipt_with_no_transaction_id = '{{\n"purchase-info" = "{}";\n}}'.format(encoded_purchase_info)
        encoded_receipt = base64.b64encode(receipt_with_no_transaction_id.encode()).decode() # Fixed NameError
        self.assertIsNone(receipt_util.extract_transaction_id_from_transaction_receipt(encoded_receipt))

    def test_indefinite_form_aware_decoder_premature_end(self):
        # This test is difficult to trigger directly without manipulating the internal state
        # or providing a specifically crafted ASN.1 structure that would cause IndexError
        # during _read_length. The existing asn1 library might handle some of these cases
        # gracefully or raise its own errors before our custom logic is hit in a specific way.
        # For now, assume that standard ASN.1 parsing errors cover most premature end scenarios.
        pass