#!/usr/bin/env python3
# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

"""
CLI tool for managing retention messages via the App Store Server API.

This tool allows you to upload, list, and delete retention messages that can be
displayed to users to encourage app re-engagement.

Example usage:
    # Upload a message with auto-generated ID
    python retention_message.py --key-id KEY123 --issuer-id ISS456 \\
        --bundle-id com.example.app --p8-file key.p8 \\
        --header "Welcome back!" --body "Check out our new features"

    # List all messages
    python retention_message.py --key-id KEY123 --issuer-id ISS456 \\
        --bundle-id com.example.app --p8-file key.p8 --action list

    # Delete a message
    python retention_message.py --key-id KEY123 --issuer-id ISS456 \\
        --bundle-id com.example.app --p8-file key.p8 \\
        --action delete --message-id abc-123-def
"""

import argparse
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Optional

# Add parent directory to path to import the library
sys.path.insert(0, str(Path(__file__).parent.parent))

from appstoreserverlibrary.api_client import AppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.models.UploadMessageRequestBody import UploadMessageRequestBody
from appstoreserverlibrary.models.UploadMessageImage import UploadMessageImage


def load_private_key(p8_file_path: str) -> bytes:
    """Load private key from .p8 file."""
    try:
        with open(p8_file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Private key file not found: {p8_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading private key file: {e}")
        sys.exit(1)


def create_api_client(args) -> AppStoreServerAPIClient:
    """Create and return an API client with the provided credentials."""
    private_key = load_private_key(args.p8_file)

    environment = Environment.SANDBOX if args.environment == 'SANDBOX' else Environment.PRODUCTION

    return AppStoreServerAPIClient(
        signing_key=private_key,
        key_id=args.key_id,
        issuer_id=args.issuer_id,
        bundle_id=args.bundle_id,
        environment=environment
    )


def upload_message(args) -> None:
    """Upload a retention message."""
    client = create_api_client(args)

    # Generate message ID if not provided
    message_id = args.message_id if args.message_id else str(uuid.uuid4())

    # Validate message length constraints
    if args.header and len(args.header) > 66:
        print(f"Error: Header text too long ({len(args.header)} chars). Maximum is 66 characters.")
        sys.exit(1)

    if args.body and len(args.body) > 144:
        print(f"Error: Body text too long ({len(args.body)} chars). Maximum is 144 characters.")
        sys.exit(1)

    if args.image_alt_text and len(args.image_alt_text) > 150:
        print(f"Error: Image alt text too long ({len(args.image_alt_text)} chars). Maximum is 150 characters.")
        sys.exit(1)

    # Create image object if image parameters provided
    image = None
    if args.image_id or args.image_alt_text:
        image = UploadMessageImage(
            imageIdentifier=args.image_id,
            altText=args.image_alt_text
        )

    # Create request body
    request_body = UploadMessageRequestBody(
        header=args.header,
        body=args.body,
        image=image
    )

    try:
        client.upload_retention_message(message_id, request_body)

        if args.json:
            print(json.dumps({
                "status": "success",
                "message_id": message_id,
                "header": args.header,
                "body": args.body,
                "environment": args.environment
            }))
        else:
            print(f"✓ Message uploaded successfully!")
            print(f"  Environment: {args.environment}")
            print(f"  Message ID: {message_id}")
            if args.header:
                print(f"  Header: {args.header}")
            if args.body:
                print(f"  Body: {args.body}")
            if image:
                print(f"  Image ID: {args.image_id}")
                print(f"  Alt Text: {args.image_alt_text}")

    except APIException as e:
        error_msg = f"API Error {e.http_status_code}"
        if e.api_error:
            error_msg += f" ({e.api_error.name})"
        if e.error_message:
            error_msg += f": {e.error_message}"

        if args.json:
            print(json.dumps({
                "status": "error",
                "error": error_msg,
                "http_status": e.http_status_code
            }))
        else:
            print(f"✗ {error_msg}")

        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({
                "status": "error",
                "error": str(e)
            }))
        else:
            print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def list_messages(args) -> None:
    """List all retention messages."""
    client = create_api_client(args)

    try:
        response = client.get_retention_message_list()

        if args.json:
            messages = []
            if response.messageIdentifiers:
                for msg in response.messageIdentifiers:
                    messages.append({
                        "message_id": msg.messageIdentifier,
                        "state": msg.messageState.value if msg.messageState else None
                    })
            print(json.dumps({
                "status": "success",
                "messages": messages,
                "total_count": len(messages),
                "environment": args.environment
            }))
        else:
            if not response.messageIdentifiers or len(response.messageIdentifiers) == 0:
                print(f"No retention messages found in {args.environment}.")
            else:
                print(f"Found {len(response.messageIdentifiers)} retention message(s) in {args.environment}:")
                print()
                for msg in response.messageIdentifiers:
                    state = msg.messageState.value if msg.messageState else "UNKNOWN"
                    print(f"  Message ID: {msg.messageIdentifier}")
                    print(f"  State:      {state}")
                    print()

    except APIException as e:
        error_msg = f"API Error {e.http_status_code}"
        if e.api_error:
            error_msg += f" ({e.api_error.name})"
        if e.error_message:
            error_msg += f": {e.error_message}"

        if args.json:
            print(json.dumps({
                "status": "error",
                "error": error_msg,
                "http_status": e.http_status_code
            }))
        else:
            print(f"✗ {error_msg}")

        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({
                "status": "error",
                "error": str(e)
            }))
        else:
            print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def delete_message(args) -> None:
    """Delete a retention message."""
    if not args.message_id:
        print("Error: --message-id is required for delete action")
        sys.exit(1)

    client = create_api_client(args)

    try:
        client.delete_retention_message(args.message_id)

        if args.json:
            print(json.dumps({
                "status": "success",
                "message_id": args.message_id,
                "action": "deleted",
                "environment": args.environment
            }))
        else:
            print(f"✓ Message deleted successfully!")
            print(f"  Environment: {args.environment}")
            print(f"  Message ID: {args.message_id}")

    except APIException as e:
        error_msg = f"API Error {e.http_status_code}"
        if e.api_error:
            error_msg += f" ({e.api_error.name})"
        if e.error_message:
            error_msg += f": {e.error_message}"

        if args.json:
            print(json.dumps({
                "status": "error",
                "error": error_msg,
                "http_status": e.http_status_code,
                "message_id": args.message_id
            }))
        else:
            print(f"✗ {error_msg}")

        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({
                "status": "error",
                "error": str(e),
                "message_id": args.message_id
            }))
        else:
            print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage App Store retention messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload a message with auto-generated ID
  %(prog)s --key-id KEY123 --issuer-id ISS456 --bundle-id com.example.app \\
           --p8-file key.p8 --header "Welcome back!" --body "New features await"

  # Upload with specific message ID and image
  %(prog)s --key-id KEY123 --issuer-id ISS456 --bundle-id com.example.app \\
           --p8-file key.p8 --message-id my-msg-001 --header "Sale!" \\
           --body "50%% off premium features" --image-id banner-001 \\
           --image-alt-text "Sale banner"

  # List all messages
  %(prog)s --key-id KEY123 --issuer-id ISS456 --bundle-id com.example.app \\
           --p8-file key.p8 --action list

  # Delete a message
  %(prog)s --key-id KEY123 --issuer-id ISS456 --bundle-id com.example.app \\
           --p8-file key.p8 --action delete --message-id my-msg-001

  # Production environment
  %(prog)s --key-id KEY123 --issuer-id ISS456 --bundle-id com.example.app \\
           --p8-file key.p8 --environment PRODUCTION --action list

Error Codes:
  4010001 - Header text too long (max 66 characters)
  4010002 - Body text too long (max 144 characters)
  4010003 - Alt text too long (max 150 characters)
  4010004 - Maximum number of messages reached
  4040001 - Message not found
  4090001 - Message with this ID already exists
        """
    )

    # Required arguments for all actions
    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument(
        '--key-id',
        required=True,
        help='Private key ID from App Store Connect (e.g., "ABCDEFGHIJ")'
    )
    required_group.add_argument(
        '--issuer-id',
        required=True,
        help='Issuer ID from App Store Connect'
    )
    required_group.add_argument(
        '--bundle-id',
        required=True,
        help='App bundle identifier (e.g., "com.example.myapp")'
    )
    required_group.add_argument(
        '--p8-file',
        required=True,
        help='Path to .p8 private key file'
    )

    # Action selection
    parser.add_argument(
        '--action',
        choices=['upload', 'list', 'delete'],
        default='upload',
        help='Action to perform (default: upload)'
    )

    # Message content arguments (for upload)
    content_group = parser.add_argument_group('message content (upload only)')
    content_group.add_argument(
        '--message-id',
        help='Unique message identifier (UUID format). Auto-generated if not provided for upload.'
    )
    content_group.add_argument(
        '--header',
        help='Header text (max 66 characters)'
    )
    content_group.add_argument(
        '--body',
        help='Body text (max 144 characters)'
    )
    content_group.add_argument(
        '--image-id',
        help='Image identifier for optional image'
    )
    content_group.add_argument(
        '--image-alt-text',
        help='Alternative text for image (max 150 characters)'
    )

    # Global options
    parser.add_argument(
        '--environment',
        choices=['SANDBOX', 'PRODUCTION'],
        default='SANDBOX',
        help='App Store environment (default: SANDBOX)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Validate arguments based on action
    if args.action == 'delete' and not args.message_id:
        parser.error("--message-id is required for delete action")

    # Validate file exists
    if not os.path.isfile(args.p8_file):
        print(f"Error: Private key file not found: {args.p8_file}")
        sys.exit(1)

    # Execute the appropriate action
    if args.action == 'upload':
        upload_message(args)
    elif args.action == 'list':
        list_messages(args)
    elif args.action == 'delete':
        delete_message(args)


if __name__ == '__main__':
    main()