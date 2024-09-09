# Apple App Store Server Python Library
The Python server library for the [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi) and [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications). Also available in [Swift](https://github.com/apple/app-store-server-library-swift), [Node.js](https://github.com/apple/app-store-server-library-node), and [Java](https://github.com/apple/app-store-server-library-java).

## Table of Contents
1. [Installation](#installation)
2. [Documentation](#documentation)
3. [Usage](#usage)
4. [Support](#support)

## Installation

#### Requirements

- Python 3.8+

### pip
```sh
pip install app-store-server-library
```

## Documentation

[Documentation](https://apple.github.io/app-store-server-library-python/)

[WWDC Video](https://developer.apple.com/videos/play/wwdc2023/10143/)

### Obtaining an In-App Purchase key from App Store Connect

To use the App Store Server API or create promotional offer signatures, a signing key downloaded from App Store Connect is required. To obtain this key, you must have the Admin role. Go to Users and Access > Integrations > In-App Purchase. Here you can create and manage keys, as well as find your issuer ID. When using a key, you'll need the key ID and issuer ID as well.

### Obtaining Apple Root Certificates

Download and store the root certificates found in the Apple Root Certificates section of the [Apple PKI](https://www.apple.com/certificateauthority/) site. Provide these certificates as an array to a SignedDataVerifier to allow verifying the signed data comes from Apple.

## Usage

### API Usage

```python
from appstoreserverlibrary.api_client import AppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
issuer_id = "99b16628-15e4-4668-972b-eeff55eeff55"
bundle_id = "com.example"
environment = Environment.SANDBOX

client = AppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment)

try:    
    response = client.request_test_notification()
    print(response)
except APIException as e:
    print(e)
```

### Verification Usage

```python
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.signed_data_verifier import VerificationException, SignedDataVerifier

root_certificates = load_root_certificates()
enable_online_checks = True
bundle_id = "com.example"
environment = Environment.SANDBOX
app_apple_id = None # appAppleId must be provided for the Production environment
signed_data_verifier = SignedDataVerifier(root_certificates, enable_online_checks, environment, bundle_id, app_apple_id)

try:    
    signed_notification = "ey.."
    payload = signed_data_verifier.verify_and_decode_notification(signed_notification)
    print(payload)
except VerificationException as e:
    print(e)
```

### Receipt Usage

```python
from appstoreserverlibrary.api_client import AppStoreServerAPIClient, APIException, GetTransactionHistoryVersion
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.receipt_utility import ReceiptUtility
from appstoreserverlibrary.models.HistoryResponse import HistoryResponse
from appstoreserverlibrary.models.TransactionHistoryRequest import TransactionHistoryRequest, ProductType, Order

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
issuer_id = "99b16628-15e4-4668-972b-eeff55eeff55"
bundle_id = "com.example"
environment = Environment.SANDBOX

client = AppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment)
receipt_util = ReceiptUtility()
app_receipt = "MI.."

try:    
    transaction_id = receipt_util.extract_transaction_id_from_app_receipt(app_receipt)
    if transaction_id != None:
        transactions = []
        response: HistoryResponse = None
        request: TransactionHistoryRequest = TransactionHistoryRequest(
            sort=Order.ASCENDING,
            revoked=False,
            productTypes=[ProductType.AUTO_RENEWABLE]
        )
        while response == None or response.hasMore:
            revision = response.revision if response != None else None
            response = client.get_transaction_history(transaction_id, revision, request, GetTransactionHistoryVersion.V2)
            for transaction in response.signedTransactions:
                transactions.append(transaction)
        print(transactions)
except APIException as e:
    print(e)

```

### Promotional Offer Signature Creation

```python
from appstoreserverlibrary.promotional_offer import PromotionalOfferSignatureCreator
import time

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
bundle_id = "com.example"

promotion_code_signature_generator = PromotionalOfferSignatureCreator(private_key, key_id, bundle_id)

product_id = "<product_id>"
subscription_offer_id = "<subscription_offer_id>"
application_username = "<application_username>"
nonce = "<nonce>"
timestamp = round(time.time()*1000)
base64_encoded_signature = promotion_code_signature_generator.create_signature(product_id, subscription_offer_id, application_username, nonce, timestamp)
```

### Async HTTPX Support

#### Pip
Include the optional async dependency
```sh
pip install app-store-server-library[async]
```

#### API Usage
```python
from appstoreserverlibrary.api_client import AsyncAppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implementation will vary

key_id = "ABCDEFGHIJ"
issuer_id = "99b16628-15e4-4668-972b-eeff55eeff55"
bundle_id = "com.example"
environment = Environment.SANDBOX

client = AsyncAppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment)

try:    
    response = await client.request_test_notification()
    print(response)
except APIException as e:
    print(e)

# Once client use is finished
await client.async_close()
```

## Support

Only the latest major version of the library will receive updates, including security updates. Therefore, it is recommended to update to new major versions.
