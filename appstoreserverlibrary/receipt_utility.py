# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from base64 import b64decode
from typing import Optional

import asn1
import base64
import re

PKCS7_OID = "1.2.840.113549.1.7.2"
IN_APP_ARRAY = 17
TRANSACTION_IDENTIFIER = 1703
ORIGINAL_TRANSACTION_IDENTIFIER = 1705

class ReceiptUtility:
    def _decode_octet_string(self, octet_string: bytes):
        decoder = asn1.Decoder()
        decoder.start(octet_string)
        _, value = decoder.read()
        return value

    def extract_transaction_id_from_app_receipt(self, app_receipt: str) -> Optional[str]:
        """
        Extracts a transaction id from an encoded App Receipt. Throws if the receipt does not match the expected format.
        *NO validation* is performed on the receipt, and any data returned should only be used to call the App Store Server API.

        :param appReceipt: The unmodified app receipt
        :return: A transaction id from the array of in-app purchases, null if the receipt contains no in-app purchases
        """
        try:
            val = self._decode_octet_string(b64decode(app_receipt, validate=True))
            found_oid = val[0]
            if found_oid != PKCS7_OID:
                raise ValueError()
            inner_value = val[1][0][2][1][0]
            # Xcode uses nested OctetStrings, we extract the inner string in this case
            value = self._decode_octet_string(inner_value)
            # We are in the top-level sequence, work our way to the array of in-apps
            for inner_value in value:
                if inner_value[0] == IN_APP_ARRAY:
                    array_values = self._decode_octet_string(inner_value[2])
                    # In-app array
                    for array_value in array_values:
                        if array_value[0] == TRANSACTION_IDENTIFIER or array_value[0] == ORIGINAL_TRANSACTION_IDENTIFIER:
                            return self._decode_octet_string(array_value[2])
            return None
        except Exception as e:
            raise ValueError(e)
    
    def extract_transaction_id_from_transaction_receipt(self, transaction_receipt: str) -> Optional[str]:
        """
        Extracts a transaction id from an encoded transactional receipt. Throws if the receipt does not match the expected format.
        *NO validation* is performed on the receipt, and any data returned should only be used to call the App Store Server API.
        :param transactionReceipt: The unmodified transactionReceipt
        :return: A transaction id, or null if no transactionId is found in the receipt
        """
        decoded_top_level = base64.b64decode(transaction_receipt).decode('utf-8')
        matching_result = re.search(r'"purchase-info"\s+=\s+"([a-zA-Z0-9+/=]+)";', decoded_top_level)
        if matching_result:
            decoded_inner_level = base64.b64decode(matching_result.group(1)).decode('utf-8')
            inner_matching_result = re.search(r'"transaction-id"\s+=\s+"([a-zA-Z0-9+/=]+)";', decoded_inner_level)
            if inner_matching_result:
                return inner_matching_result.group(1)
        return None
