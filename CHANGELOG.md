# Changelog

## Version 1.8.0
- Incorporate changes for App Store Server API v1.15 and App Store Server Notifications v2.15 [https://github.com/apple/app-store-server-library-python/pull/134]

## Version 1.7.0
- Update the SignedDataVerifier to cache verified certificate chains, improving performance [https://github.com/apple/app-store-server-library-python/pull/122]

## Version 1.6.0
- Update README to improve Dependabot link discovery [https://github.com/apple/app-store-server-library-python/pull/119]

## Version 1.5.0
- Add an async client built on httpx [https://github.com/apple/app-store-server-library-python/pull/105]
- Drop Python 3.7 support [https://github.com/apple/app-store-server-library-python/pull/106]
- Add check for original transaction id in legacy receipts [https://github.com/apple/app-store-server-library-python/pull/104] from @willhnation

## Version 1.4.0
- Incorporate changes for App Store Server API v1.13 and App Store Server Notifications v2.13 [https://github.com/apple/app-store-server-library-python/pull/102]
- Remove the upper limit on libraries that are unlikely to break upon upgrade [https://github.com/apple/app-store-server-library-python/pull/101]

## Version 1.3.0
- Incorporate changes for App Store Server API v1.12 and App Store Server Notifications v2.12 [https://github.com/apple/app-store-server-library-python/pull/95]
- Fix deprecation warnings from cryptography [https://github.com/apple/app-store-server-library-python/pull/94] from @WFT
- Replace use of deprecated datetime.utcnow() [https://github.com/apple/app-store-server-library-python/pull/93] from @WFT
- Cache cattrs values to prevent memory leak [https://github.com/apple/app-store-server-library-python/pull/92] from @Reskov

## Version 1.2.1
- Fix issue with OfferType in JWSTransactionDecodedPayload [https://github.com/apple/app-store-server-library-python/pull/88] from @devinwang

## Version 1.2.0
- Incorporate changes for App Store Server API v1.11 and App Store Server Notifications v2.11 [https://github.com/apple/app-store-server-library-python/pull/85]
- Various documentation and quality of life improvements, including contributions from @CallumWatkins, @hakusai22, and @sunny-dubey

## Version 1.1.0
- Support App Store Server Notifications v2.10 [https://github.com/apple/app-store-server-library-python/pull/65]
- Bump cryptography and pyOpenSSL maximum versions [https://github.com/apple/app-store-server-library-python/pull/61]/[https://github.com/apple/app-store-server-library-python/pull/63]
- Require appAppleId in SignedDataVerifier for the Production environment [https://github.com/apple/app-store-server-library-python/pull/60]

## 1.0.0
- Add error message to APIException [https://github.com/apple/app-store-server-library-python/pull/52]

## 0.3.0
- Add missing status field to the Data model [https://github.com/apple/app-store-server-library-python/pull/33]
- Add error codes from App Store Server API v1.9 [https://github.com/apple/app-store-server-library-python/pull/39]
- Add new fields from App Store Server API v1.10 [https://github.com/apple/app-store-server-library-python/pull/46]
- Add support for reading unknown enum values [https://github.com/apple/app-store-server-library-python/pull/45]
- Add support for Xcode and LocalTesting environments [https://github.com/apple/app-store-server-library-python/pull/44]

## 0.2.1
- Add py.typed file [https://github.com/apple/app-store-server-library-python/pull/19]
- Correct type annotation in PromotionalOfferSignatureCreator [https://github.com/apple/app-store-server-library-python/pull/17]

## 0.2.0

- Correct type in LastTransactionsItem's status field [https://github.com/apple/app-store-server-library-python/pull/11]
- Fix default value None for fields should require an Optional type [https://github.com/apple/app-store-server-library-python/pull/6]
