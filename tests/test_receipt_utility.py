# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import base64
import unittest

import asn1

from appstoreserverlibrary.receipt_utility import ReceiptUtility

from tests.util import read_data_from_file

APP_RECEIPT_EXPECTED_TRANSACTION_ID = "0"
TRANSACTION_RECEIPT_EXPECTED_TRANSACTION_ID = "33993399"

def _encode_attribute(encoder: asn1.Encoder, attribute_type: int, value: bytes):
    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(attribute_type, asn1.Numbers.Integer)
    encoder.write(1, asn1.Numbers.Integer)
    encoder.write(value, asn1.Numbers.OctetString)
    encoder.leave()

def _encode_value(value, value_type: asn1.Numbers) -> bytes:
    encoder = asn1.Encoder()
    encoder.start()
    encoder.write(value, value_type)
    return encoder.output()

def _encode_attributes(attribute_type: int, value: bytes, container_type: asn1.Numbers = asn1.Numbers.Set) -> bytes:
    encoder = asn1.Encoder()
    encoder.start()
    encoder.enter(container_type)
    _encode_attribute(encoder, attribute_type, value)
    encoder.leave()
    return encoder.output()

def _create_app_receipt(payload: bytes) -> str:
    encoder = asn1.Encoder()
    encoder.start()
    encoder.enter(asn1.Numbers.Sequence)
    encoder.write("1.2.840.113549.1.7.2", asn1.Numbers.ObjectIdentifier)
    encoder.enter(0, asn1.Classes.Context)
    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(1, asn1.Numbers.Integer)
    encoder.enter(asn1.Numbers.Set)
    encoder.leave()
    encoder.enter(asn1.Numbers.Sequence)
    encoder.write("1.2.840.113549.1.7.1", asn1.Numbers.ObjectIdentifier)
    encoder.enter(0, asn1.Classes.Context)
    encoder.write(payload, asn1.Numbers.OctetString)
    encoder.leave()
    encoder.leave()
    encoder.leave()
    encoder.leave()
    encoder.leave()
    return base64.b64encode(encoder.output()).decode('utf-8')

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

    def test_app_receipt_extraction_with_unexpected_content_type(self):
        encoder = asn1.Encoder()
        encoder.start()
        encoder.enter(asn1.Numbers.Sequence)
        encoder.write("1.2.840.113549.1.7.1", asn1.Numbers.ObjectIdentifier)
        encoder.leave()
        receipt = base64.b64encode(encoder.output()).decode('utf-8')

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt(receipt)

    def test_app_receipt_extraction_with_invalid_base64(self):
        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt("not a receipt")

    def test_app_receipt_extraction_with_valid_base64_that_is_not_asn1(self):
        receipt = base64.b64encode(b'not a PKCS#7 container').decode('utf-8')

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt(receipt)

    def test_app_receipt_extraction_with_empty_receipt(self):
        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt("")

    def test_app_receipt_extraction_with_transaction_receipt(self):
        receipt = read_data_from_file("tests/resources/mock_signed_data/legacyTransaction")

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt(receipt)

    def test_transaction_receipt_extraction_without_purchase_info(self):
        receipt = base64.b64encode(b'{\n\t"signature" = "c2lnbmF0dXJl";\n}').decode('utf-8')

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_transaction_receipt(receipt)

    def test_transaction_receipt_extraction_with_invalid_base64(self):
        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_transaction_receipt("not a receipt")

    def test_transaction_receipt_extraction_with_empty_receipt(self):
        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_transaction_receipt("")

    def test_transaction_receipt_extraction_with_non_utf8_content(self):
        receipt = base64.b64encode(b'\xff\xfe\x00"purchase-info"').decode('utf-8')

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_transaction_receipt(receipt)

    def test_transaction_receipt_extraction_with_malformed_purchase_info(self):
        receipt = base64.b64encode(b'{\n\t"purchase-info" = "abc";\n}').decode('utf-8')

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_transaction_receipt(receipt)

    def test_transaction_receipt_extraction_with_app_receipt(self):
        receipt = read_data_from_file("tests/resources/xcode/xcode-app-receipt-with-transaction")

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_transaction_receipt(receipt)

    def test_transaction_receipt_extraction_without_transaction_id(self):
        purchase_info = base64.b64encode(b'{\n\t"product-id" = "com.example.product";\n}').decode('utf-8')
        receipt = base64.b64encode(('{\n\t"purchase-info" = "' + purchase_info + '";\n}').encode('utf-8')).decode('utf-8')

        receipt_util = ReceiptUtility()

        extracted_transaction_id = receipt_util.extract_transaction_id_from_transaction_receipt(receipt)

        self.assertIsNone(extracted_transaction_id)

    def test_app_receipt_extraction_with_utf8_string_transaction_id(self):
        receipt = _create_app_receipt(_encode_attributes(17, _encode_attributes(1703, _encode_value("2000000000000001", asn1.Numbers.UTF8String))))

        receipt_util = ReceiptUtility()

        extracted_transaction_id = receipt_util.extract_transaction_id_from_app_receipt(receipt)

        self.assertEqual("2000000000000001", extracted_transaction_id)

    def test_app_receipt_extraction_with_transaction_id_that_is_not_a_utf8_string(self):
        receipt_util = ReceiptUtility()

        for value, value_type in [(2000000000000001, asn1.Numbers.Integer), (b'2000000000000001', asn1.Numbers.OctetString), ("2000000000000001", asn1.Numbers.IA5String)]:
            receipt = _create_app_receipt(_encode_attributes(17, _encode_attributes(1703, _encode_value(value, value_type))))
            with self.subTest(value_type=value_type), self.assertRaises(ValueError):
                receipt_util.extract_transaction_id_from_app_receipt(receipt)

    def test_app_receipt_extraction_with_in_app_purchase_receipt_that_is_not_a_set(self):
        receipt = _create_app_receipt(_encode_attributes(17, _encode_value("not a set", asn1.Numbers.UTF8String)))

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt(receipt)

    def test_app_receipt_extraction_with_payload_that_is_not_a_set(self):
        receipt = _create_app_receipt(_encode_attributes(17, _encode_attributes(1703, _encode_value("2000000000000001", asn1.Numbers.UTF8String)), asn1.Numbers.Sequence))

        receipt_util = ReceiptUtility()

        with self.assertRaises(ValueError):
            receipt_util.extract_transaction_id_from_app_receipt(receipt)
