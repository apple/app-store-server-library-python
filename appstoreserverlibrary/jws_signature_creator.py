# Copyright (c) 2025 Apple Inc. Licensed under MIT License.

import datetime
from typing import Any, Dict, Optional
import base64
import json
import jwt
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from appstoreserverlibrary.models.LibraryUtility import _get_cattrs_converter

class AdvancedCommerceAPIInAppRequest:
    def __init__(self):
        pass

class JWSSignatureCreator:
    def __init__(self, audience: str, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str):
        self._audience = audience
        self._signing_key = serialization.load_pem_private_key(signing_key, password=None, backend=default_backend())
        self._key_id = key_id
        self._issuer_id = issuer_id
        self._bundle_id = bundle_id

    def _create_signature(self, feature_specific_claims: Dict[str, Any]) -> str:
        claims = feature_specific_claims
        current_time = datetime.datetime.now(datetime.timezone.utc)

        claims["bid"] = self._bundle_id
        claims["iss"] = self._issuer_id
        claims["aud"] = self._audience
        claims["iat"] = current_time
        claims["nonce"] = str(uuid.uuid4())

        return jwt.encode(claims,
            self._signing_key,
            algorithm="ES256",
            headers={"kid": self._key_id},
        )
    
class PromotionalOfferV2SignatureCreator(JWSSignatureCreator):
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str):
        """
        Create a PromotionalOfferV2SignatureCreator

        :param signing_key: Your private key downloaded from App Store Connect
        :param key_id: Your private key ID from App Store Connect
        :param issuer_id: Your issuer ID from the Keys page in App Store Connect
        :param bundle_id: Your app's bundle ID
        """
        super().__init__(audience="promotional-offer", signing_key=signing_key, key_id=key_id, issuer_id=issuer_id, bundle_id=bundle_id)

    def create_signature(self, product_id: str, offer_identifier: str, transaction_id: Optional[str]) -> str:
        """
        Create a promotional offer V2 signature.
        https://developer.apple.com/documentation/storekit/generating-jws-to-sign-app-store-requests
        
        :param product_id: The unique identifier of the product
        :param offer_identifier: The promotional offer identifier that you set up in App Store Connect
        :param transaction_id: The unique identifier of any transaction that belongs to the customer. You can use the customer's appTransactionId, even for customers who haven't made any In-App Purchases in your app. This field is optional, but recommended.
        :return: The signed JWS.
        """
        if product_id is None:
            raise ValueError("product_id cannot be null")
        if offer_identifier is None:
            raise ValueError("offer_identifier cannot be null")
        feature_specific_claims = {
            "productId": product_id,
            "offerIdentifier": offer_identifier
        }
        if transaction_id is not None:
            feature_specific_claims["transactionId"] = transaction_id
        return self._create_signature(feature_specific_claims=feature_specific_claims)
    
class IntroductoryOfferEligibilitySignatureCreator(JWSSignatureCreator):
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str):
        """
        Create an IntroductoryOfferEligibilitySignatureCreator

        :param signing_key: Your private key downloaded from App Store Connect
        :param key_id: Your private key ID from App Store Connect
        :param issuer_id: Your issuer ID from the Keys page in App Store Connect
        :param bundle_id: Your app's bundle ID
        """
        super().__init__(audience="introductory-offer-eligibility", signing_key=signing_key, key_id=key_id, issuer_id=issuer_id, bundle_id=bundle_id)

    def create_signature(self, product_id: str, allow_introductory_offer: bool, transaction_id: str) -> str:
        """
        Create an introductory offer eligibility signature.
        https://developer.apple.com/documentation/storekit/generating-jws-to-sign-app-store-requests
        
        :param product_id: The unique identifier of the product
        :param allow_introductory_offer: A boolean value that determines whether the customer is eligible for an introductory offer
        :param transaction_id: The unique identifier of any transaction that belongs to the customer. You can use the customer's appTransactionId, even for customers who haven't made any In-App Purchases in your app.
        :return: The signed JWS.
        """
        if product_id is None:
            raise ValueError("product_id cannot be null")
        if allow_introductory_offer is None:
            raise ValueError("allow_introductory_offer cannot be null")
        if transaction_id is None:
            raise ValueError("transaction_id cannot be null")
        feature_specific_claims = {
            "productId": product_id,
            "allowIntroductoryOffer": allow_introductory_offer,
            "transactionId": transaction_id
        }
        return self._create_signature(feature_specific_claims=feature_specific_claims)
    
class AdvancedCommerceAPIInAppSignatureCreator(JWSSignatureCreator):
    def __init__(self, signing_key: bytes, key_id: str, issuer_id: str, bundle_id: str):
        """
        Create an AdvancedCommerceAPIInAppSignatureCreator

        :param signing_key: Your private key downloaded from App Store Connect
        :param key_id: Your private key ID from App Store Connect
        :param issuer_id: Your issuer ID from the Keys page in App Store Connect
        :param bundle_id: Your app's bundle ID
        """
        super().__init__(audience="advanced-commerce-api", signing_key=signing_key, key_id=key_id, issuer_id=issuer_id, bundle_id=bundle_id)

    def create_signature(self, advanced_commerce_in_app_request: AdvancedCommerceAPIInAppRequest) -> str:
        """
        Create an Advanced Commerce in-app signed request.
        https://developer.apple.com/documentation/storekit/generating-jws-to-sign-app-store-requests
        
        :param advanced_commerce_in_app_request: The request to be signed.
        :return: The signed JWS.
        """
        if advanced_commerce_in_app_request is None:
            raise ValueError("advanced_commerce_in_app_request cannot be null")
        c = _get_cattrs_converter(type(advanced_commerce_in_app_request))
        request = c.unstructure(advanced_commerce_in_app_request)
        encoded_request = base64.b64encode(json.dumps(request).encode(encoding='utf-8')).decode('utf-8')
        feature_specific_claims = {
            "request": encoded_request
        }
        return self._create_signature(feature_specific_claims=feature_specific_claims)