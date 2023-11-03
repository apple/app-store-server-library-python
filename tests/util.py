# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from typing import Any, Dict
import jwt
from jwt.api_jwt import decode_complete
import json
import os

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from appstoreserverlibrary.models.Environment import Environment

from appstoreserverlibrary.signed_data_verifier import SignedDataVerifier

def create_signed_data_from_json(path: str) -> str:
    data = read_data_from_file(path)
    decoded_data = json.loads(data)
    private_key = ec.generate_private_key(ES256).private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption()).decode()
    return jwt.encode(payload=decoded_data, key=private_key, algorithm='ES256')

def decode_json_from_signed_date(data: str) -> Dict[str, Any]:
    public_key = ec.generate_private_key(ES256).public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    return decode_complete(jwt=data, key=public_key, algorithms=['ES256'], options={"verify_signature": False})

def read_data_from_file(path: str) -> str:
    full_path = os.path.join(path)
    with open(full_path, mode='r') as test_file:
        return test_file.read()
    
def read_data_from_binary_file(path: str) -> str:
    full_path = os.path.join(path)
    with open(full_path, mode='rb') as test_file:
        return test_file.read()

class ES256(ec.EllipticCurve):
    name="prime256v1"
    key_size = 256

def get_signed_data_verifier(env: Environment, bundle_id: str, app_apple_id: int = 1234) -> SignedDataVerifier:
    verifier = SignedDataVerifier([read_data_from_binary_file('tests/resources/certs/testCA.der')], False, env, bundle_id, app_apple_id)
    verifier._chain_verifier.enable_strict_checks = False # We don't have authority identifiers on test certs
    return verifier

def get_default_signed_data_verifier():
    return get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example")