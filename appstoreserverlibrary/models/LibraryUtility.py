# Copyright (c) 2023 Apple Inc. Licensed under MIT License.

from enum import EnumMeta
from functools import lru_cache
from typing import Any, List, Type, TypeVar

from attr import Attribute, has, ib, fields
from cattr import override
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override
import cattrs

T = TypeVar('T')

metadata_key = 'correspondingFieldName'
metadata_type_key = 'typeOfField'

class AppStoreServerLibraryEnumMeta(EnumMeta):
    def __contains__(c, val):
        try:
            c(val)
        except ValueError:
            return False
        return True

    def create_main_attr(c, raw_field_name: str) -> Any:
        def value_set(self, _: Attribute, value: c):
            newValue = value.value if value is not None else None
            if newValue != getattr(self, raw_field_name):
                object.__setattr__(self, raw_field_name, newValue)
            return value
        return ib(default=None, on_setattr=value_set, metadata={metadata_key: raw_field_name, metadata_type_key: 'main'})
    
    def create_raw_attr(c, field_name: str) -> Any:
        def value_set(self, _: Attribute, value: str):
            newValue = c(value) if value in c else None
            if newValue != getattr(self, field_name):
                object.__setattr__(self, field_name, newValue)
            return value
        return ib(default=None, kw_only=True, on_setattr=value_set, metadata={metadata_key: field_name, metadata_type_key: 'raw'})
    
class AttrsRawValueAware:
    def __attrs_post_init__(self):
        attr_fields: List[Attribute] = fields(type(self))
        for attribute in attr_fields:
            if attribute.metadata.get(metadata_type_key) != 'raw':
                continue
            field: str = attribute.metadata[metadata_key]
            raw_field = f'raw{field[0].upper()}{field[1:]}'

            if (raw_value := getattr(self, raw_field)) is not None:
                setattr(self, raw_field, raw_value)
            elif (value := getattr(self, field)) is not None:
                setattr(self, field, value)


@lru_cache(maxsize=None)
def _get_cattrs_converter(destination_class: Type[T]) -> cattrs.Converter:
    c = cattrs.Converter()
    attributes: List[Attribute] = fields(destination_class)
    cattrs_overrides = {}
    for attribute in attributes:
        if attribute.metadata.get(metadata_type_key) == 'raw':
            matching_name: str = attribute.metadata[metadata_key]
            cattrs_overrides[matching_name] = override(omit=True)
            raw_field = f'raw{matching_name[0].upper()}{matching_name[1:]}'
            cattrs_overrides[raw_field] = override(rename=matching_name)
    c.register_structure_hook_factory(has, lambda cl: make_dict_structure_fn(cl, c, **cattrs_overrides))
    c.register_unstructure_hook_factory(has, lambda cl: make_dict_unstructure_fn(cl, c, **cattrs_overrides))
    return c