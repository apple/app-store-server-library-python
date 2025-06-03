# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

import unittest
import base64 # Make sure base64 is imported
import json # For crafting JWS header
from base64 import b64decode
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.NotificationHistoryRequest import NotificationTypeV2
from appstoreserverlibrary.models.ResponseBodyV2DecodedPayload import ResponseBodyV2DecodedPayload
from appstoreserverlibrary.models.Summary import Summary
from appstoreserverlibrary.models.ExternalPurchaseToken import ExternalPurchaseToken

from appstoreserverlibrary.signed_data_verifier import VerificationException, VerificationStatus, SignedDataVerifier

from tests.util import get_signed_data_verifier, read_data_from_file, read_data_from_binary_file, create_signed_data_from_json # Added create_signed_data_from_json

class PayloadVerification(unittest.TestCase):
    def test_app_store_server_notification_decoding(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        test_notification = read_data_from_file('tests/resources/mock_signed_data/testNotification')
        notification = verifier.verify_and_decode_notification(test_notification)
        self.assertEqual(notification.notificationType, NotificationTypeV2.TEST)

    def test_app_store_server_notification_decoding_production(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example")
        test_notification = read_data_from_file('tests/resources/mock_signed_data/testNotification')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(test_notification)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

    def test_missing_x5c_header(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        missing_x5c_header_claim = read_data_from_file('tests/resources/mock_signed_data/missingX5CHeaderClaim')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(missing_x5c_header_claim)
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_wrong_bundle_id_for_server_notification(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.examplex")
        wrong_bundle = read_data_from_file('tests/resources/mock_signed_data/wrongBundleId')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(wrong_bundle)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_wrong_app_apple_id_for_server_notification(self):
        verifier = get_signed_data_verifier(Environment.PRODUCTION, "com.example", 1235)
        test_notification = read_data_from_file('tests/resources/mock_signed_data/testNotification')
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification(test_notification)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_renewal_info_decoding(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        renewal_info = read_data_from_file('tests/resources/mock_signed_data/renewalInfo')
        notification = verifier.verify_and_decode_renewal_info(renewal_info)
        self.assertEqual(notification.environment, Environment.SANDBOX)

    def test_transaction_info_decoding(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        transaction_info = read_data_from_file('tests/resources/mock_signed_data/transactionInfo')
        notification = verifier.verify_and_decode_signed_transaction(transaction_info)
        self.assertEqual(notification.environment, Environment.SANDBOX)

    def test_renewal_info_invalid_environment(self):
        # Use Environment.XCODE to allow easy payload modification without re-signing
        # The actual signed JWS for renewalInfo is for SANDBOX
        verifier = get_signed_data_verifier(Environment.XCODE, "com.example")
        renewal_info_signed = read_data_from_file('tests/resources/mock_signed_data/renewalInfo')

        # Modify the verifier's environment to be PRODUCTION to create a mismatch
        verifier._environment = Environment.PRODUCTION

        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_renewal_info(renewal_info_signed)

        raised_exception = context.exception
        self.assertEqual(raised_exception.status, VerificationStatus.INVALID_ENVIRONMENT)
        expected_message = "Verification failed with status " + VerificationStatus.INVALID_ENVIRONMENT.name
        self.assertEqual(str(raised_exception), expected_message) # Ensures __str__ is called
        self.assertEqual(raised_exception.status.value, 6) # Ensures status attribute is accessed


    def test_transaction_info_invalid_bundle_id(self):
        # Use Environment.XCODE to allow easy payload modification
        # The actual signed JWS for transactionInfo is for "com.example"
        verifier = get_signed_data_verifier(Environment.XCODE, "com.different.app") # Verifier expects different bundle ID
        transaction_info_signed = read_data_from_file('tests/resources/mock_signed_data/transactionInfo')

        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_signed_transaction(transaction_info_signed)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)
        self.assertTrue("Verification failed with status INVALID_APP_IDENTIFIER" in str(context.exception))

    def test_transaction_info_invalid_environment(self):
        # Use Environment.XCODE to allow easy payload modification
        # The actual signed JWS for transactionInfo is for SANDBOX
        verifier = get_signed_data_verifier(Environment.XCODE, "com.example")
        transaction_info_signed = read_data_from_file('tests/resources/mock_signed_data/transactionInfo')

        # Modify the verifier's environment to be PRODUCTION to create a mismatch
        verifier._environment = Environment.PRODUCTION

        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_signed_transaction(transaction_info_signed)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)
        self.assertTrue("Verification failed with status INVALID_ENVIRONMENT" in str(context.exception))

    def test_malformed_jwt_with_too_many_parts(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification("a.b.c.d")
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_malformed_jwt_with_malformed_data(self):
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example")
        with self.assertRaises(VerificationException) as context:
            verifier.verify_and_decode_notification("a.b.c")
        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)

    def test_production_verifier_requires_app_apple_id(self):
        with self.assertRaisesRegex(ValueError, "appAppleId is required when the environment is Production"):
            SignedDataVerifier(root_certificates=[], enable_online_checks=False, environment=Environment.PRODUCTION, bundle_id="com.example")

    def test_verifier_with_no_root_certs_throws_if_not_xcode_localtesting(self):
        # For an environment that requires chain verification
        with self.assertRaises(VerificationException) as context:
            verifier = SignedDataVerifier(root_certificates=[], enable_online_checks=False, environment=Environment.SANDBOX, bundle_id="com.example")
            # Minimal valid JWS structure to pass initial parsing and x5c checks in _decode_signed_object
            # Header: {"alg":"ES256","x5c":["validCertInBase64"]} Payload: {} Signature: (anything)
            # Using a short, non-empty x5c array.
            minimal_jws = "eyJhbGciOiJFUzI1NiIsIng1YyI6WyJYSVgwZEdWa2VTQkRaR1Z5WTJWeWRDQmQiXX0.e30.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
            verifier._decode_signed_object(minimal_jws)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_CERTIFICATE)

    def test_verifier_with_no_root_certs_ok_for_xcode(self):
        try:
            verifier = SignedDataVerifier(root_certificates=[], enable_online_checks=False, environment=Environment.XCODE, bundle_id="com.example")
            # This should not raise INVALID_CERTIFICATE for XCODE env
            decoded = verifier._decode_signed_object(read_data_from_file('tests/resources/xcode/xcode-signed-transaction'))
            self.assertIsNotNone(decoded)
        except VerificationException as e:
            self.fail(f"Should not raise VerificationException for XCODE env, but got {e.status}")


    def test_cache_pruning_and_expiration(self):
        import time
        from appstoreserverlibrary.signed_data_verifier import _ChainVerifier
        from tests.util import read_data_from_binary_file # Corrected import

        root_certs_data = [read_data_from_binary_file('tests/resources/certs/testCA.der')] # Corrected file read
        chain_verifier = _ChainVerifier(root_certificates=root_certs_data)

        # Fill the cache
        for i in range(_ChainVerifier.MAXIMUM_CACHE_SIZE + 5):
            # Create slightly different cert chains to ensure different cache keys
            certs = [f"cert0_{i}", f"cert1_{i}", f"cert2_{i}"]
            chain_verifier.verified_certificates_cache[tuple(certs)] = (f"key_{i}", time.time() + _ChainVerifier.CACHE_TIME_LIMIT)

        self.assertEqual(len(chain_verifier.verified_certificates_cache), _ChainVerifier.MAXIMUM_CACHE_SIZE + 5)

        # Trigger pruning by adding one more
        certs_new = ["new_cert0", "new_cert1", "new_cert2"]
        chain_verifier.put_verified_public_key(certs_new, "new_key")
        # At this point, if pruning happened due to size, it would be because all existing were non-expired
        # The current pruning logic only removes expired items when oversized.
        # So, let's expire some items manually to test that part of pruning

        keys_to_expire = list(chain_verifier.verified_certificates_cache.keys())[:5]
        for key_to_expire in keys_to_expire:
            original_value = chain_verifier.verified_certificates_cache[key_to_expire]
            chain_verifier.verified_certificates_cache[key_to_expire] = (original_value[0], time.time() - 1) # Expired

        # Add another to trigger pruning of expired items
        chain_verifier.put_verified_public_key(["another_new_0", "another_new_1", "another_new_2"], "another_new_key")

        # After adding "another_new_key", the size was MAX_SIZE + 5 + 1 (certs_new) + 1 (another_new_key) = MAX_SIZE + 7
        # Then, 5 expired items were removed.
        # So, final size should be MAX_SIZE + 7 - 5 = MAX_SIZE + 2
        self.assertEqual(len(chain_verifier.verified_certificates_cache), _ChainVerifier.MAXIMUM_CACHE_SIZE + 2)

        # Test cache expiration in get_cached_public_key
        expired_key_tuple = keys_to_expire[0]
        self.assertIsNone(chain_verifier.get_cached_public_key(list(expired_key_tuple))) # Should be None as it's expired

        # Test getting a valid (non-expired) key
        valid_key_tuple = tuple(certs_new)
        self.assertEqual(chain_verifier.get_cached_public_key(list(valid_key_tuple)), "new_key")

    def test_app_store_server_notification_decoding_summary(self):
        # Data from signedSummaryNotification.json:
        # bundleId: "com.example", appAppleId: 41234, environment: "LocalTesting"
        # We use create_signed_data_from_json, so signature is test-generated.
        # Verifier must match these details, use LOCAL_TESTING or XCODE.
        verifier = get_signed_data_verifier(Environment.LOCAL_TESTING, "com.example", 41234)
        summary_payload_path = 'tests/resources/models/signedSummaryNotification.json'
        signed_summary_notification = create_signed_data_from_json(summary_payload_path)

        notification = verifier.verify_and_decode_notification(signed_summary_notification)
        self.assertIsNotNone(notification.summary)
        self.assertEqual(notification.summary.bundleId, "com.example")
        self.assertEqual(notification.summary.environment, Environment.LOCAL_TESTING)
        self.assertEqual(notification.summary.appAppleId, 41234)
        self.assertEqual(notification.notificationType, NotificationTypeV2.RENEWAL_EXTENSION)
        self.assertEqual(notification.subtype, "SUMMARY")


    def test_app_store_server_notification_decoding_external_purchase_token(self):
        # Test handling of notifications with externalPurchaseToken

        # Scenario 1: Token implies PRODUCTION environment, verifier is LOCAL_TESTING
        # This test ensures that the fields are extracted from externalPurchaseToken (lines 101-103),
        # the environment is derived as PRODUCTION (line 106),
        # and then _verify_notification correctly identifies an environment mismatch.
        prod_ept_payload_path = 'tests/resources/models/signedExternalPurchaseTokenNotification.json'
        prod_ept_payload_content = json.loads(read_data_from_file(prod_ept_payload_path))
        prod_ept_bundle_id = prod_ept_payload_content["externalPurchaseToken"]["bundleId"]
        prod_ept_app_apple_id = prod_ept_payload_content["externalPurchaseToken"]["appAppleId"]

        signed_prod_ept = create_signed_data_from_json(prod_ept_payload_path)

        verifier_local_for_prod_token = get_signed_data_verifier(Environment.LOCAL_TESTING, prod_ept_bundle_id, prod_ept_app_apple_id)
        with self.assertRaises(VerificationException) as context:
            verifier_local_for_prod_token.verify_and_decode_notification(signed_prod_ept)
        self.assertEqual(context.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

        # Scenario 2: Token implies SANDBOX environment, verifier is LOCAL_TESTING
        # This test ensures that the fields are extracted (lines 101-103),
        # the environment is derived as SANDBOX (line 104),
        # and then _verify_notification correctly identifies an environment mismatch.
        sandbox_ept_payload_path = 'tests/resources/models/signedExternalPurchaseTokenSandboxNotification.json'
        sandbox_ept_payload_content = json.loads(read_data_from_file(sandbox_ept_payload_path))
        sandbox_ept_bundle_id = sandbox_ept_payload_content["externalPurchaseToken"]["bundleId"]
        sandbox_ept_app_apple_id = sandbox_ept_payload_content["externalPurchaseToken"]["appAppleId"]

        signed_sandbox_ept = create_signed_data_from_json(sandbox_ept_payload_path)

        verifier_local_for_sandbox_token = get_signed_data_verifier(Environment.LOCAL_TESTING, sandbox_ept_bundle_id, sandbox_ept_app_apple_id)
        with self.assertRaises(VerificationException) as context_sandbox:
            verifier_local_for_sandbox_token.verify_and_decode_notification(signed_sandbox_ept)
        self.assertEqual(context_sandbox.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

        # Scenario 3: Verifying the content of a decoded EPT using an XCODE verifier
        # This allows us to inspect the ResponseBodyV2DecodedPayload object itself,
        # as XCODE verifier will allow environment mismatch during _verify_notification to pass if bundle ID is okay.
        # We need to ensure the verifier's bundle ID and appAppleId match the token's for this specific check.

        # For PRODUCTION derived token:
        verifier_xcode_prod = get_signed_data_verifier(Environment.XCODE, prod_ept_bundle_id, prod_ept_app_apple_id)
        # We need to ensure _verify_notification passes or fails predictably.
        # If verifier is XCODE, derived is PROD -> _verify_notification will throw INVALID_ENVIRONMENT
        # So, we can't get the object back from verify_and_decode_notification directly if environments don't match.

        # The previous two scenarios (LOCAL_TESTING verifier) already cover lines 101-106 because the exception
        # occurs in _verify_notification, which is called *after* these lines.
        # To assert the *contents* of externalPurchaseToken after decoding, we must ensure _verify_notification passes.
        # This requires the verifier's environment to match the token's derived environment.
        # Since create_signed_data_from_json doesn't create real signed tokens, we must use XCODE/LOCAL_TESTING
        # for the main verifier if we want _decode_signed_object to succeed without x5c.
        # This leads to a situation where _verify_notification will *always* fail for EPTs if their
        # derived environment is PROD/SANDBOX and verifier is XCODE/LOCAL_TESTING.

        # Let's use the fact that Summary notifications *can* have LOCAL_TESTING environment.
        # We'll assume lines 101-103 (bundleId, appAppleId, externalPurchaseId access) are covered
        # if the code reaches line 104 or 106. The exceptions above prove this.

        # Direct tests for _verify_notification logic for an EPT payload
        # (Simulating that an EPT was decoded and these values were extracted)
        token_bundle_id = "com.example.ept"
        token_app_apple_id = 77777

        # Case A: Derived PRODUCTION, Verifier PRODUCTION - MATCH
        prod_derived_env = Environment.PRODUCTION
        verifier_prod_match = SignedDataVerifier([], False, Environment.PRODUCTION, token_bundle_id, token_app_apple_id)
        try:
            verifier_prod_match._verify_notification(token_bundle_id, token_app_apple_id, prod_derived_env)
        except VerificationException:
            self.fail("_verify_notification failed for EPT: PRODUCTION verifier, PRODUCTION token data")

        # Case B: Derived SANDBOX, Verifier SANDBOX - MATCH
        sandbox_derived_env = Environment.SANDBOX
        verifier_sandbox_match = SignedDataVerifier([], False, Environment.SANDBOX, token_bundle_id, token_app_apple_id)
        try:
            verifier_sandbox_match._verify_notification(token_bundle_id, token_app_apple_id, sandbox_derived_env)
        except VerificationException:
            self.fail("_verify_notification failed for EPT: SANDBOX verifier, SANDBOX token data")

        # Case C: Derived PRODUCTION, Verifier SANDBOX - MISMATCH
        with self.assertRaises(VerificationException) as ctx_env_mismatch:
            verifier_sandbox_match._verify_notification(token_bundle_id, token_app_apple_id, prod_derived_env)
        self.assertEqual(ctx_env_mismatch.exception.status, VerificationStatus.INVALID_ENVIRONMENT)

        # Case D: Derived PRODUCTION, Verifier PRODUCTION, Bundle ID MISMATCH
        verifier_bundle_mismatch = SignedDataVerifier([], False, Environment.PRODUCTION, "com.wrong.bundle", token_app_apple_id)
        with self.assertRaises(VerificationException) as ctx_bundle:
            verifier_bundle_mismatch._verify_notification(token_bundle_id, token_app_apple_id, prod_derived_env)
        self.assertEqual(ctx_bundle.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

        # Case E: Derived PRODUCTION, Verifier PRODUCTION, AppAppleId MISMATCH
        verifier_appid_mismatch = SignedDataVerifier([], False, Environment.PRODUCTION, token_bundle_id, 88888)
        with self.assertRaises(VerificationException) as ctx_appid:
            verifier_appid_mismatch._verify_notification(token_bundle_id, token_app_apple_id, prod_derived_env)
        self.assertEqual(ctx_appid.exception.status, VerificationStatus.INVALID_APP_IDENTIFIER)

    def test_decode_signed_object_invalid_alg_header(self):
        # Using SANDBOX environment for verifier, but _decode_signed_object will use XCODE-like path for non-Apple certs if needed
        # However, these JWS are structurally invalid before signature check, so error is from jwt.decode or header checks
        verifier = get_signed_data_verifier(Environment.SANDBOX, "com.example", 123) # Needs app_apple_id for PRODUCTION path if certs were real

        # Case 1: No alg header
        # Header: {"kid":"somekid","x5c":["abc"]} (alg missing)
        header_no_alg_bytes = b'{"kid":"somekid","x5c":["YSBiIGM="]}' # x5c: "a b c"
        header_no_alg = base64.urlsafe_b64encode(header_no_alg_bytes).decode('utf-8').rstrip("=")
        jws_no_alg = f"{header_no_alg}.e30.e30" # e30 is base64url({})

        with self.assertRaises(VerificationException) as context_no_alg:
            verifier._decode_signed_object(jws_no_alg)
        self.assertEqual(context_no_alg.exception.status, VerificationStatus.VERIFICATION_FAILURE)
        self.assertTrue("Algorithm was not ES256" in str(context_no_alg.exception.__cause__))

        # Case 2: alg is not ES256
        # Header: {"alg":"RS256","kid":"somekid","x5c":["abc"]}
        header_wrong_alg_bytes = b'{"alg":"RS256","kid":"somekid","x5c":["YSBiIGM="]}'
        header_wrong_alg = base64.urlsafe_b64encode(header_wrong_alg_bytes).decode('utf-8').rstrip("=")
        jws_wrong_alg = f"{header_wrong_alg}.e30.e30"
        with self.assertRaises(VerificationException) as context_wrong_alg:
            verifier._decode_signed_object(jws_wrong_alg)
        self.assertEqual(context_wrong_alg.exception.status, VerificationStatus.VERIFICATION_FAILURE)
        self.assertTrue("Algorithm was not ES256" in str(context_wrong_alg.exception.__cause__))

    def test_decode_signed_object_effective_date_no_online_no_signed_date(self):
        # Covers path: not self._enable_online_checks and (signed_date is None and receiptCreationDate is None)
        # So effective_date should become time.time()
        root_certs_bytes = [read_data_from_binary_file('tests/resources/certs/testCA.der')]
        verifier = SignedDataVerifier(root_certificates=root_certs_bytes,
                                      enable_online_checks=False, # Important for this test
                                      environment=Environment.SANDBOX, # Not XCODE, so chain verification is attempted
                                      bundle_id="com.example",
                                      app_apple_id=123) # app_apple_id needed for non-Xcode production

        # Payload: {"otherField":"value"}
        payload_b64_no_date = base64.urlsafe_b64encode(b'{"otherField":"value"}').decode('utf-8').rstrip("=")

        # Create an x5c header with valid base64 encoded DER certificates (use testCA for all 3)
        cert_der_bytes = read_data_from_binary_file('tests/resources/certs/testCA.der')
        cert_b64_str = base64.b64encode(cert_der_bytes).decode('utf-8')
        x5c_array = [cert_b64_str, cert_b64_str, cert_b64_str]

        header_obj = {
            "alg": "ES256",
            "x5c": x5c_array
        }
        header_b64 = base64.urlsafe_b64encode(json.dumps(header_obj).encode('utf-8')).decode('utf-8').rstrip("=")

        dummy_sig = "dummySignature" # This signature will not match the certs
        jws_no_signed_date = f"{header_b64}.{payload_b64_no_date}.{dummy_sig}"

        # We expect VERIFICATION_FAILURE. This could be due to OID checks failing,
        # or ultimately the final jwt.decode failing because the dummy signature doesn't match the public key
        # from the (now parsable) certificates in x5c. The key is that we get past line 131.
        # The important part for this test is that the code path for effective_date calculation is hit.
        # If enable_online_checks=False and signedDate is None, effective_date becomes time.time().
        # The subsequent chain validation will use this effective_date.
        with self.assertRaises(VerificationException) as context:
            verifier._decode_signed_object(jws_no_signed_date)

        self.assertEqual(context.exception.status, VerificationStatus.VERIFICATION_FAILURE)
        # We can't easily assert effective_date was time.time() without mocking time or deeper inspection,
        # but reaching VERIFICATION_FAILURE means the line was executed.
        # The line 131 calculates effective_date. If enable_online_checks=False and no signedDate,
        # effective_date becomes time.time(). This is then passed to _chain_verifier.verify_chain.
        # The verify_chain will then likely fail due to OID checks or other reasons with these test certs,
        # leading to VERIFICATION_FAILURE. If it passed OID somehow, the final jwt.decode would fail on signature.

if __name__ == '__main__':
    unittest.main()
