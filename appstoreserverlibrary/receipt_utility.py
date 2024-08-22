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
    def extract_transaction_id_from_app_receipt(self, app_receipt: str) -> Optional[str]:
        """
        Extracts a transaction id from an encoded App Receipt. Throws if the receipt does not match the expected format.
        *NO validation* is performed on the receipt, and any data returned should only be used to call the App Store Server API.

        :param appReceipt: The unmodified app receipt
        :return: A transaction id from the array of in-app purchases, null if the receipt contains no in-app purchases
        """
        decoder = IndefiniteFormAwareDecoder()
        decoder.start(b64decode(app_receipt, validate=True))
        tag = decoder.peek()
        if tag.typ != asn1.Types.Constructed or tag.nr != asn1.Numbers.Sequence:
            raise ValueError()
        decoder.enter()
        # PKCS#7 object
        tag, value = decoder.read()
        if tag.typ != asn1.Types.Primitive or tag.nr != asn1.Numbers.ObjectIdentifier or value != PKCS7_OID:
            raise ValueError()
        # This is the PKCS#7 format, work our way into the inner content
        decoder.enter()
        decoder.enter()
        decoder.read()
        decoder.read()
        decoder.enter()
        decoder.read()
        decoder.enter()
        tag, value = decoder.read()
        # Xcode uses nested OctetStrings, we extract the inner string in this case
        if tag.typ == asn1.Types.Constructed and tag.nr == asn1.Numbers.OctetString:
            inner_decoder = asn1.Decoder()
            inner_decoder.start(value)
            tag, value = inner_decoder.read()
        if tag.typ != asn1.Types.Primitive or tag.nr != asn1.Numbers.OctetString:
            raise ValueError()
        decoder = asn1.Decoder()
        decoder.start(value)
        tag = decoder.peek()
        if tag.typ != asn1.Types.Constructed or tag.nr != asn1.Numbers.Set:
            raise ValueError()
        decoder.enter()
        # We are in the top-level sequence, work our way to the array of in-apps
        while not decoder.eof():
            decoder.enter()
            tag, value = decoder.read()
            if tag.typ == asn1.Types.Primitive and tag.nr == asn1.Numbers.Integer and value == IN_APP_ARRAY:
                decoder.read()
                tag, value = decoder.read()
                if tag.typ != asn1.Types.Primitive or tag.nr != asn1.Numbers.OctetString:
                    raise ValueError()
                inapp_decoder = asn1.Decoder()
                inapp_decoder.start(value)
                inapp_decoder.enter()
                # In-app array
                while not inapp_decoder.eof():
                    inapp_decoder.enter()
                    tag, value = inapp_decoder.read()
                    if (
                        tag.typ == asn1.Types.Primitive
                        and tag.nr == asn1.Numbers.Integer
                        and (value == TRANSACTION_IDENTIFIER or value == ORIGINAL_TRANSACTION_IDENTIFIER)
                    ):
                        inapp_decoder.read()
                        tag, value = inapp_decoder.read()
                        singleton_decoder = asn1.Decoder()
                        singleton_decoder.start(value)
                        tag, value = singleton_decoder.read()
                        return value
                    inapp_decoder.leave()
            decoder.leave()
        return None
    
    def extract_transaction_id_from_transaction_receipt(self, transaction_receipt: str) -> Optional[str]:
        """
        Extracts a transaction id from an encoded transactional receipt. Throws if the receipt does not match the expected format.
        *NO validation* is performed on the receipt, and any data returned should only be used to call the App Store Server API.
        :param transactionReceipt: The unmodified transactionReceipt
        :return: A transaction id, or null if no transactionId is found in the receipt
        """
        decoded_top_level = base64.b64decode(transaction_receipt).decode('utf-8')
        matching_result = re.search('"purchase-info"\s+=\s+"([a-zA-Z0-9+/=]+)";', decoded_top_level)
        if matching_result:
            decoded_inner_level = base64.b64decode(matching_result.group(1)).decode('utf-8')
            inner_matching_result = re.search('"transaction-id"\s+=\s+"([a-zA-Z0-9+/=]+)";', decoded_inner_level)
            if inner_matching_result:
                return inner_matching_result.group(1)
        return None

class IndefiniteFormAwareDecoder(asn1.Decoder):
    def _read_length(self) -> int:
        index, input_data = self.m_stack[-1]
        try:
            byte = input_data[index]
        except IndexError:
            raise asn1.Error('Premature end of input.')
        if byte == 0x80:
            # Xcode receipts use indefinite length encoding, not supported by all parsers
            # Indefinite length encoding is only entered, but never left during parsing for receipts
            # We therefore round up indefinite length encoding to be the remaining length
            self._read_byte()
            index, input_data = self.m_stack[-1]
            return len(input_data) - index
        return super()._read_length()