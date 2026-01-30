# Copyright (c) 2026 Apple Inc. Licensed under MIT License.

from typing import TypeVar

T = TypeVar('T')


class AdvancedCommerceValidationUtils:
    MAXIMUM_DESCRIPTION_LENGTH = 45
    MAXIMUM_DISPLAY_NAME_LENGTH = 30
    MAXIMUM_SKU_LENGTH = 128
    MIN_PERIOD = 1
    MAX_PERIOD = 12

    @staticmethod
    def description_validator(instance, attribute, value):
        """
        Validates description is not None and does not exceed maximum length.

        Raises:
            ValueError: If description exceeds maximum length
        """
        if len(value) > AdvancedCommerceValidationUtils.MAXIMUM_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description length cannot exceed "
                f"{AdvancedCommerceValidationUtils.MAXIMUM_DESCRIPTION_LENGTH} characters"
            )

    @staticmethod
    def display_name_validator(instance, attribute, value):
        """
        Validates display name is not None and does not exceed maximum length.

        Raises:
            ValueError: If display name exceeds maximum length
        """
        if len(value) > AdvancedCommerceValidationUtils.MAXIMUM_DISPLAY_NAME_LENGTH:
            raise ValueError(
                f"Display name length cannot exceed "
                f"{AdvancedCommerceValidationUtils.MAXIMUM_DISPLAY_NAME_LENGTH} characters"
            )

    @staticmethod
    def sku_validator(instance, attribute, value):
        """
        Validates SKU does not exceed maximum length.

        Raises:
            ValueError: If SKU exceeds maximum length
        """
        if len(value) > AdvancedCommerceValidationUtils.MAXIMUM_SKU_LENGTH:
            raise ValueError(
                f"SKU length cannot exceed "
                f"{AdvancedCommerceValidationUtils.MAXIMUM_SKU_LENGTH} characters"
            )

    @staticmethod
    def period_count_validator(instance, attribute, value):
        """
        Validates periodCount is not None and between `MIN_PERIOD` and `MAX_PERIOD` inclusive.

        Raises:
            ValueError: If period_count is out of range
        """
        if (value < AdvancedCommerceValidationUtils.MIN_PERIOD or
            value > AdvancedCommerceValidationUtils.MAX_PERIOD):
            raise ValueError(
                f"Period count must be between "
                f"{AdvancedCommerceValidationUtils.MIN_PERIOD} and "
                f"{AdvancedCommerceValidationUtils.MAX_PERIOD}"
            )

    @staticmethod
    def items_validator(instance, attribute, value):
        """
        Validates a list of items is not None, not empty, and contains no None elements.

        Raises:
            ValueError: If list is empty or contains None elements
        """
        if not value:
            raise ValueError("Items list cannot be empty")

        for i, item in enumerate(value):
            if item is None:
                raise ValueError(f"Item at index {i} in the list cannot be None")

    @staticmethod
    def dependent_skus_validator(instance, attribute, value):
        """
        Validates that each SKU in the dependentSKUs list does not exceed maximum length.

        Raises:
            ValueError: If any SKU exceeds maximum length
        """
        for sku in value:
            if len(sku) > AdvancedCommerceValidationUtils.MAXIMUM_SKU_LENGTH:
                raise ValueError(
                    f"SKU length cannot exceed "
                    f"{AdvancedCommerceValidationUtils.MAXIMUM_SKU_LENGTH} characters"
                )
