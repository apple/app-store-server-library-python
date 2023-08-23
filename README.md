# Apple App Store Server Python Library
The Python server library for the [App Store Server API](https://developer.apple.com/documentation/appstoreserverapi) and [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications)

## Table of Contents
1. [Beta](#-beta-)
2. [Installation](#installation)
3. [Documentation](#documentation)
4. [Usage](#usage)
5. [Support](#support)

## ⚠️ Beta ⚠️

This software is currently in Beta testing. Therefore, it should only be used for testing purposes, like for the Sandbox environment. API signatures may change between releases and signature verification may receive security updates. 

## Installation

#### Requirements

- Python 3.7+

### Gradle
```groovy
pip install app-store-server-library
```

## Documentation

[Documentation](https://apple.github.io/app-store-server-library-python/)

[WWDC Video](https://developer.apple.com/videos/play/wwdc2023/10143/)
## Usage

### API Usage

```python
from appstoreserverlibrary.api_client import AppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.SendTestNotificationResponse import SendTestNotificationResponse

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implemenation will vary

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
signed_data_verifier = SignedDataVerifier(root_certificates, enable_online_checks, environment, bundle_id)

try:    
    signed_notification = "ey.."
    payload = signed_data_verifier.verify_and_decode_notification()
    print(payload)
except VerificationException as e:
    print(e)
```

### Receipt Usage

```python
from appstoreserverlibrary.api_client import AppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.receipt_utility import ReceiptUtility
from appstoreserverlibrary.models.HistoryResponse import HistoryResponse
from appstoreserverlibrary.models.TransactionHistoryRequest import TransactionHistoryRequest, ProductType, Order

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implemenation will vary

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
            response = client.get_transaction_history(transaction_id, revision, request)
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

private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8") # Implemenation will vary

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

## Support

Only the latest major version of the library will receive updates, including security updates. Therefore, it is recommended to update to new major versions.
