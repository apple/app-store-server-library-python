# CLI Tools for App Store Server Library

This directory contains command-line tools for interacting with the App Store Server API.

## Retention Message Tool

The `retention_message.py` tool allows you to manage retention messages that can be displayed to users to encourage app re-engagement.

### Prerequisites

1. **App Store Connect Credentials**: You need:
   - Private Key ID (`key_id`) from App Store Connect
   - Issuer ID (`issuer_id`) from App Store Connect
   - Your app's Bundle ID (`bundle_id`)
   - Private key file (`.p8` format) downloaded from App Store Connect

2. **Python Dependencies**: Make sure the app-store-server-library is installed:
   ```bash
   pip install -r ../requirements.txt
   ```

### Usage

#### Upload a Retention Message

Upload a new retention message with auto-generated ID:
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/SubscriptionKey_ABCDEFGHIJ.p8" \
  --header "Welcome back!" \
  --body "Check out our new features"
```

Upload with a specific message ID:
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --message-id "my-campaign-001" \
  --header "Limited Time Sale!" \
  --body "50% off premium features this week"
```

Upload with an image:
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --header "New Update!" \
  --body "Amazing new features await" \
  --image-id "banner-v2" \
  --image-alt-text "App update banner showing new features"
```

#### List All Messages

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action list
```

#### Delete a Message

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action delete \
  --message-id "my-campaign-001"
```

#### Configure Default Messages

Set a message as the default for a specific product and locale. The default message is shown when the real-time messaging flow isn't available or fails.

**Single Product:**
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action set-default \
  --message-id "my-campaign-001" \
  --product-id "com.example.premium" \
  --locale "en-US"
```

**Multiple Products (Bulk Operation):**
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action set-default \
  --message-id "my-campaign-001" \
  --product-id "com.example.premium" \
  --product-id "com.example.basic" \
  --product-id "com.example.pro" \
  --locale "en-US"
```

#### Delete Default Message Configuration

Remove the default message configuration for one or more products:

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action delete-default \
  --product-id "com.example.premium" \
  --product-id "com.example.basic" \
  --locale "en-US"
```

### Environment Options

By default, the tool uses the **SANDBOX** environment. For production:

```bash
python retention_message.py \
  --environment PRODUCTION \
  # ... other parameters
```

### Output Formats

#### Human-Readable (default)
```
✓ Message uploaded successfully!
  Message ID: abc-123-def
  Header: Welcome back!
  Body: Check out our new features
```

#### JSON Format
Use `--json` for programmatic usage:
```bash
python retention_message.py --json --action list # ... other params
```

Output:
```json
{
  "status": "success",
  "messages": [
    {
      "message_id": "abc-123-def",
      "state": "PENDING"
    }
  ],
  "total_count": 1
}
```

### Message States

Messages can be in one of three states:
- **PENDING**: Message uploaded and awaiting Apple's review
- **APPROVED**: Message approved and can be shown to users
- **REJECTED**: Message rejected and cannot be used

### Constraints and Limits

- **Header text**: Maximum 66 characters
- **Body text**: Maximum 144 characters
- **Image alt text**: Maximum 150 characters
- **Message ID**: Must be unique (UUIDs recommended)
- **Total messages**: Limited number per app (see Apple's documentation)

### Error Handling

The tool provides clear error messages for common issues:

| Error Code | Description | Solution |
|------------|-------------|----------|
| 4000023 | Invalid product ID | Verify product ID exists in App Store Connect |
| 4000164 | Invalid locale | Use valid locale code (e.g., "en-US", "fr-FR") |
| 4010001 | Header text too long | Reduce header to ≤66 characters |
| 4010002 | Body text too long | Reduce body to ≤144 characters |
| 4010003 | Alt text too long | Reduce alt text to ≤150 characters |
| 4010004 | Maximum messages reached | Delete old messages first |
| 4030017 | Message not approved | Wait for Apple approval before setting as default |
| 4030018 | Image not approved | Wait for Apple approval of associated image |
| 4040001 | Message not found | Check message ID spelling |
| 4090001 | Message ID already exists | Use a different message ID |

### Security Notes

- **Never commit** your `.p8` private key files to version control
- Store credentials securely (consider using environment variables)
- Use sandbox environment for testing
- Be cautious with production environment operations

### Troubleshooting

1. **"Private key file not found"**
   - Verify the path to your `.p8` file is correct
   - Ensure the file exists and is readable

2. **"Invalid app identifier"**
   - Check that your bundle ID matches exactly
   - Verify the bundle ID is configured in App Store Connect

3. **Authentication errors**
   - Verify your Key ID and Issuer ID are correct
   - Ensure your private key corresponds to the Key ID
   - Check that the key has appropriate permissions

4. **"Message not found" when deleting**
   - List messages first to see available IDs
   - Ensure you're using the correct environment (sandbox vs production)

### Examples for Different Use Cases

#### A/B Testing Messages
```bash
# Upload message A
python retention_message.py --message-id "test-a-v1" \
  --header "Come back!" --body "We miss you" # ... other params

# Upload message B
python retention_message.py --message-id "test-b-v1" \
  --header "New features!" --body "Check out what's new" # ... other params
```

#### Seasonal Campaigns
```bash
# Holiday campaign
python retention_message.py --message-id "holiday-2023" \
  --header "Holiday Sale!" --body "Limited time: 40% off premium" # ... other params

# Back to school
python retention_message.py --message-id "back-to-school-2023" \
  --header "Ready to learn?" --body "New study tools available" # ... other params
```

#### Setting Default Messages Across Multiple Tiers

Apply the same message to all subscription tiers in a single command:

```bash
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --action set-default --message-id "general-retention-v1" \
  --product-id "com.example.basic" \
  --product-id "com.example.premium" \
  --product-id "com.example.pro" \
  --locale "en-US"
```

Output for bulk operations:
```
✓ Default message configured successfully for 3 product(s)!
  Environment: SANDBOX
  Message ID: general-retention-v1
  Locale:     en-US
  Products:   com.example.basic, com.example.premium, com.example.pro
```

### Integration with CI/CD

For automated deployments, use JSON output:

```bash
#!/bin/bash
RESULT=$(python retention_message.py --json --action upload \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --header "Auto-deployed message" --body "Latest features")

if echo "$RESULT" | jq -e '.status == "success"' > /dev/null; then
  echo "Message deployed successfully"
  MESSAGE_ID=$(echo "$RESULT" | jq -r '.message_id')
  echo "Message ID: $MESSAGE_ID"
else
  echo "Deployment failed"
  exit 1
fi
```

## Future Tools

This directory is designed to be expanded with additional CLI tools for other App Store Server API functionality as needed.