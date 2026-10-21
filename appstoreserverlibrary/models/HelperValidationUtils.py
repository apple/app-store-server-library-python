# Copyright (c) 2026 Apple Inc. Licensed under MIT License.


class HelperValidationUtils:
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
            ValueError: If description is None or exceeds maximum length
        """
        if value is None:
            raise ValueError("Description cannot be None")
        if len(value) > HelperValidationUtils.MAXIMUM_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description length cannot exceed "
                f"{HelperValidationUtils.MAXIMUM_DESCRIPTION_LENGTH} characters"
            )

    @staticmethod
    def display_name_validator(instance, attribute, value):
        """
        Validates display name is not None and does not exceed maximum length.

        Raises:
            ValueError: If display name is None or exceeds maximum length
        """
        if value is None:
            raise ValueError("Display name cannot be None")
        if len(value) > HelperValidationUtils.MAXIMUM_DISPLAY_NAME_LENGTH:
            raise ValueError(
                f"Display name length cannot exceed "
                f"{HelperValidationUtils.MAXIMUM_DISPLAY_NAME_LENGTH} characters"
            )

    @staticmethod
    def sku_validator(instance, attribute, value):
        """
        Validates SKU is not None and does not exceed maximum length.

        Raises:
            ValueError: If SKU is None or exceeds maximum length
        """
        if value is None:
            raise ValueError("SKU cannot be None")
        if len(value) > HelperValidationUtils.MAXIMUM_SKU_LENGTH:
            raise ValueError(
                f"SKU length cannot exceed "
                f"{HelperValidationUtils.MAXIMUM_SKU_LENGTH} characters"
            )

    @staticmethod
    def period_count_validator(instance, attribute, value):
        """
        Validates periodCount is an integer between `MIN_PERIOD` and `MAX_PERIOD` inclusive.

        Raises:
            ValueError: If period_count is not an integer or is out of range
        """
        if value is None:
            raise ValueError("Period count cannot be None")
        if (not isinstance(value, int) or isinstance(value, bool) or
            value < HelperValidationUtils.MIN_PERIOD or
            value > HelperValidationUtils.MAX_PERIOD):
            raise ValueError(
                f"Period count must be an integer between "
                f"{HelperValidationUtils.MIN_PERIOD} and "
                f"{HelperValidationUtils.MAX_PERIOD}"
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
        Validates that each SKU in the dependentSKUs list is not None and does not exceed maximum length.

        Raises:
            ValueError: If any SKU is None or exceeds maximum length
        """
        for i, sku in enumerate(value):
            if sku is None:
                raise ValueError(f"Item at index {i} in the list cannot be None")
            if len(sku) > HelperValidationUtils.MAXIMUM_SKU_LENGTH:
                raise ValueError(
                    f"SKU length cannot exceed "
                    f"{HelperValidationUtils.MAXIMUM_SKU_LENGTH} characters"
                )
