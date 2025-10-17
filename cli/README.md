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
  --header "Don't miss out!" \
  --body "Keep enjoying unlimited access to all premium content"
```

Upload with a specific message ID:
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --message-id "550e8400-e29b-41d4-a716-446655440001" \
  --header "Stay subscribed and save" \
  --body "Your subscription gives you access to exclusive features"
```

Upload with an image:
```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --message-id "550e8400-e29b-41d4-a716-446655440002" \
  --header "You'll lose access to" \
  --body "Premium content, ad-free experience, and exclusive features" \
  --image-id "6ba7b810-9dad-11d1-80b4-00c04fd430c8" \
  --image-alt-text "Visual showing premium features and content library"
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
  --message-id "550e8400-e29b-41d4-a716-446655440001"
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
  --message-id "550e8400-e29b-41d4-a716-446655440003" \
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
  --message-id "550e8400-e29b-41d4-a716-446655440003" \
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

### Image Operations

Images can be uploaded and associated with text-based retention messages to make them more visually engaging.

#### Upload an Image

Upload a PNG image for use in retention messages with auto-generated ID:

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action upload-image \
  --image-file "/path/to/premium_features_banner.png"
```

Upload with a specific image ID:

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action upload-image \
  --image-id "6ba7b810-9dad-11d1-80b4-00c04fd430c8" \
  --image-file "/path/to/premium_features_banner.png"
```

**Image Requirements:**
- **Format**: PNG only
- **Dimensions**: Exactly 3840 × 2160 pixels
- **Transparency**: Not allowed
- **Maximum images**: 2000 per app

After upload, images are in **PENDING** state awaiting Apple approval. In SANDBOX, they're auto-approved.

#### List All Images

Check the status of all uploaded images:

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action list-images
```

Output:
```
Found 2 retention image(s) in SANDBOX:

  Image ID: banner-2024-q1
  State:    APPROVED

  Image ID: promo-summer
  State:    PENDING
```

#### Delete an Image

Delete a previously uploaded image (must not be in use by any message):

```bash
python retention_message.py \
  --key-id "ABCDEFGHIJ" \
  --issuer-id "12345678-1234-1234-1234-123456789012" \
  --bundle-id "com.example.myapp" \
  --p8-file "/path/to/key.p8" \
  --action delete-image \
  --image-id "6ba7b810-9dad-11d1-80b4-00c04fd430c7"
```

**Important**: You must delete any messages that reference an image before you can delete the image itself.

#### Complete Workflow: Message with Image

Here's the complete workflow for creating a retention message with an image:

```bash
# Step 1: Upload the image
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --action upload-image \
  --image-id "7ba7b810-9dad-11d1-80b4-00c04fd430c9" \
  --image-file "./images/premium_benefits_showcase.png"

# Step 2: Check image approval status (skip in SANDBOX as it's auto-approved)
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --action list-images

# Step 3: Upload a message that references the image
# Note: Both --header and --body are REQUIRED
# Note: --image-id and --image-alt-text must be provided together
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --action upload \
  --message-id "650e8400-e29b-41d4-a716-446655440040" \
  --header "Keep all your benefits" \
  --body "Continue enjoying unlimited streaming and exclusive content" \
  --image-id "7ba7b810-9dad-11d1-80b4-00c04fd430c9" \
  --image-alt-text "Collage of premium features including ad-free streaming and exclusive shows"

# Step 4: Set as default for products (optional)
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --action set-default \
  --message-id "650e8400-e29b-41d4-a716-446655440040" \
  --product-id "com.example.premium" \
  --locale "en-US"
```

#### Image States

Images can be in one of three states:
- **PENDING**: Image uploaded and awaiting Apple's review
- **APPROVED**: Image approved and can be used in messages
- **REJECTED**: Image rejected and cannot be used

Both the message and its associated image must be in **APPROVED** state before the system can display them.

#### Image Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| 4000104 | Invalid image | Ensure PNG format, 3840×2160 pixels, no transparency |
| 4030002 | Image in use | Delete messages using this image first |
| 4030019 | Maximum images reached | Delete unused images (limit: 2000) |
| 4040002 | Image not found | Check image ID spelling |
| 4090002 | Image ID already exists | Use a different image ID |

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

**Required Fields (for upload action):**
- **Header text**: REQUIRED - Maximum 66 characters
- **Body text**: REQUIRED - Maximum 144 characters

**Optional Fields:**
- **Image reference**: Optional - Use `--image-id` and `--image-alt-text` together
- **Image alt text**: Maximum 150 characters (required if image is included)
- **Message ID**: Must be unique (UUIDs recommended, auto-generated if not provided)

**System Limits:**
- **Total messages**: 2000 per app
- **Total images**: 2000 per app

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
# Upload message A - Emotional appeal
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --message-id "550e8400-e29b-41d4-a716-446655440010" \
  --header "We value your membership" \
  --body "Continue enjoying premium benefits and exclusive content"

# Upload message B - Value-focused
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --message-id "550e8400-e29b-41d4-a716-446655440011" \
  --header "Keep your premium access" \
  --body "Ad-free experience, offline downloads, and more"
```

#### Seasonal Campaigns
```bash
# Holiday campaign - Highlight seasonal content
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --message-id "550e8400-e29b-41d4-a716-446655440020" \
  --header "Holiday content awaits" \
  --body "Stay subscribed for exclusive seasonal features"

# Back to school - Educational content retention
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --message-id "550e8400-e29b-41d4-a716-446655440021" \
  --header "Your learning continues" \
  --body "Keep accessing study tools and educational resources"
```

#### Setting Default Messages Across Multiple Tiers

Apply the same message to all subscription tiers in a single command:

```bash
python retention_message.py \
  --key-id "$KEY_ID" --issuer-id "$ISSUER_ID" \
  --bundle-id "$BUNDLE_ID" --p8-file "$P8_FILE" \
  --action set-default \
  --message-id "550e8400-e29b-41d4-a716-446655440030" \
  --product-id "com.example.basic" \
  --product-id "com.example.premium" \
  --product-id "com.example.pro" \
  --locale "en-US"
```

Output for bulk operations:
```
✓ Default message configured successfully for 3 product(s)!
  Environment: SANDBOX
  Message ID: 550e8400-e29b-41d4-a716-446655440030
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
  --message-id "750e8400-e29b-41d4-a716-446655440050" \
  --header "Stay connected" \
  --body "Keep your subscription active for uninterrupted access")

if echo "$RESULT" | jq -e '.status == "success"' > /dev/null; then
  echo "Retention message deployed successfully"
  MESSAGE_ID=$(echo "$RESULT" | jq -r '.message_id')
  echo "Message ID: $MESSAGE_ID"
else
  echo "Deployment failed"
  exit 1
fi
```

## Future Tools

This directory is designed to be expanded with additional CLI tools for other App Store Server API functionality as needed.