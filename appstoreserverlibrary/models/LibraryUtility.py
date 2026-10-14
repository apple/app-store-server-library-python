# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import EnumMeta
from functools import lru_cache
from typing import Any, List, Type, TypeVar
from uuid import UUID

from attr import Attribute, has, ib, fields
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override
import cattrs

T = TypeVar('T')

metadata_key = 'correspondingFieldName'
metadata_type_key = 'typeOfField'
metadata_required_key = 'requiredField'
metadata_none_value_key = 'serializedValueWhenNone'

def validate_not_none(instance, attribute: Attribute, value):
    if value is None:
        raise ValueError(f"{attribute.name} cannot be None")

def _structure_required_value(value: Any, cl: Type[T]) -> T:
    if value is None:
        raise ValueError()
    return cl(value)

class AppStoreServerLibraryEnumMeta(EnumMeta):
    def __contains__(c, val):
        try:
            c(val)
        except ValueError:
            return False
        return True  
    
    def create_main_attr(c, raw_field_name: str, raw_required: bool = False, kw_only: bool = False) -> Any:
        def value_set(self, attribute: Attribute, value: c):
            newValue = value.value if value is not None else None
            if raw_required and newValue is None:
                raise ValueError(f"{attribute.name} cannot be set to None when field is required")
            if newValue != getattr(self, raw_field_name):
                object.__setattr__(self, raw_field_name, newValue)
            return value
        return ib(default=None, kw_only=kw_only, on_setattr=value_set, metadata={metadata_key: raw_field_name, metadata_type_key: 'main'})

    def create_raw_attr(c, field_name: str, required: bool = False) -> Any:
        def value_set(self, _: Attribute, value: str):
            if required and value is None:
                raise ValueError(f"raw{field_name[0].upper() + field_name[1:]} cannot be None")
            newValue = c(value) if value in c else None
            if newValue != getattr(self, field_name):
                object.__setattr__(self, field_name, newValue)
            return value

        if required:
            from attr import Factory
            def factory(instance):
                main_value = getattr(instance, field_name)
                if main_value is not None:
                    return main_value.value
                raise ValueError(f"Either {field_name} or raw{field_name[0].upper() + field_name[1:]} must be provided")
            return ib(default=Factory(factory, takes_self=True), kw_only=True, on_setattr=value_set, validator=validate_not_none, metadata={metadata_key: field_name, metadata_type_key: 'raw', metadata_required_key: True})
        else:
            return ib(default=None, kw_only=True, on_setattr=value_set, metadata={metadata_key: field_name, metadata_type_key: 'raw', metadata_required_key: False})
    
class AttrsRawValueAware:
    def __attrs_post_init__(self):
        attr_fields: List[Attribute] = fields(type(self))
        for attribute in attr_fields:
            if metadata_type_key not in attribute.metadata or attribute.metadata[metadata_type_key] != 'raw':
                continue
            field: str = attribute.metadata.get(metadata_key)
            rawField = 'raw' + field[0].upper() + field[1:]
            rawValue = getattr(self, rawField)
            value = getattr(self, field)
            if rawValue is not None:
                setattr(self, rawField, rawValue)
            elif value is not None:
                setattr(self, field, value)


@lru_cache(maxsize=None)
def _get_cattrs_converter(destination_class: Type[T]) -> cattrs.Converter:
    c = cattrs.Converter()

    # Register UUID hooks to ensure lowercase serialization
    c.register_unstructure_hook(UUID, lambda uuid: str(uuid).lower() if uuid is not None else None)

    for required_type in (str, int, float, bool, UUID):
        c.register_structure_hook(required_type, _structure_required_value)

    # Need a function here because it must be a lambda based on cl, which is not always destination_class
    def make_overrides(cl):
        attributes: List[Attribute] = fields(cl)
        cattrs_overrides = {}
        # Use omit_if_default to prevent null fields from being serialized to JSON
        for attribute in attributes:
            if metadata_type_key in attribute.metadata:
                matching_name: str = attribute.metadata[metadata_key]
                if attribute.metadata[metadata_type_key] == 'raw':
                    cattrs_overrides[matching_name] = override(omit=True)
                    raw_field = 'raw' + matching_name[0].upper() + matching_name[1:]
                    if attribute.metadata.get(metadata_required_key, False):
                        cattrs_overrides[raw_field] = override(rename=matching_name)
                    else:
                        cattrs_overrides[raw_field] = override(rename=matching_name, omit_if_default=True)
            elif not attribute.init and attribute.name not in cattrs_overrides:
                cattrs_overrides[attribute.name] = override(omit=False)
            elif metadata_none_value_key in attribute.metadata and attribute.name not in cattrs_overrides:
                none_value = attribute.metadata[metadata_none_value_key]
                cattrs_overrides[attribute.name] = override(unstruct_hook=lambda value, none_value=none_value: none_value if value is None else c.unstructure(value))
            elif attribute.default is None and attribute.name not in cattrs_overrides:
                cattrs_overrides[attribute.name] = override(omit_if_default=True)
        return cattrs_overrides

    c.register_structure_hook_factory(has, lambda cl: make_dict_structure_fn(cl, c, **make_overrides(cl)))
    c.register_unstructure_hook_factory(has, lambda cl: make_dict_unstructure_fn(cl, c, **make_overrides(cl)))
    return c
