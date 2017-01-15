# -*- coding: utf-8 -*-
import functools
import json
from . import exc


class Field(object):

    def __init__(self,
                 name,
                 dtype=unicode,
                 default=None,
                 required=False,
                 validator=None,
                 **kwargs):
        self.name = name
        self.default = default
        self.required = required
        self.validator = validator

        if isinstance(dtype, list):
            self.dtype = dtype[0]
            self.listed = True
        else:
            self.dtype = dtype
            self.listed = False

        self.min_value = kwargs.get('min_value')
        self.max_value = kwargs.get('max_value')
        self.choices = kwargs.get('choices')

        self.min_len = kwargs.get('min_len')
        self.max_len = kwargs.get('max_len')
        self.len_cut = kwargs.get('len_cut')

        self.min_list_len = kwargs.get('min_list_len')
        self.max_list_len = kwargs.get('max_list_len')
        self.list_cut = kwargs.get('list_cut')

    def parse_value(self, input_value):
        if input_value is None or (self.listed and len(input_value) < 1):
            if self.default is not None:
                if self.validator:
                    return validate(self.validator, self.name, self.default)
                return self.default
            if self.required:
                raise exc.InputError(exc.Code.INPUT_MISSING, self.name)
            return None

        if self.listed:
            value = self.validate_list(
                [self.validate_single_value(v) for v in input_value]
            )
        else:
            value = self.validate_single_value(input_value)

        if self.validator:
            value = validate(self.validator, self.name, input_value)

        return value

    def validate_single_value(self, value):
        try:
            if self.dtype == bool:
                value = json.loads(value)
            value = self.dtype(value)
        except:
            raise exc.InputError(exc.Code.INPUT_TYPE_INVALID, self.name)
        if self.min_value is not None and value < self.min_value:
            raise exc.InputError(exc.Code.INPUT_LT_MIN, self.name)

        if self.max_value is not None and value > self.max_value:
            raise exc.InputError(exc.Code.INPUT_GT_MAX, self.name)

        if self.choices and value not in self.choices:
            raise exc.InputError(exc.Code.INPUT_NOT_IN_CHOICES, self.name)

        if self.min_len is not None and len(value) < self.min_len:
            raise exc.InputError(exc.Code.INPUT_LT_MIN_LEN, self.name)

        if self.max_len is not None and len(value) > self.max_len:
            if not self.len_cut:
                raise exc.InputError(exc.Code.INPUT_GT_MAX_LEN, self.name)
            value = value[:self.max_len]

        return value

    def validate_list(self, values):
        if self.min_list_len is not None and len(values) < self.min_list_len:
            raise exc.InputError(exc.Code.INPUT_LT_MIN_LIST_LEN, self.name)
        if self.max_list_len is not None and len(values) > self.max_list_len:
            if not self.list_cut:
                raise exc.InputError(exc.Code.INPUT_GT_MAX_LIST_LEN, self.name)
            values = values[:self.max_list_len]
        return values


class ArgumentsGroup(object):

    def __init__(self, *groups):
        self.groups = groups

    def parse_arguments(self, handler):
        if not self.groups:
            return {}
        for group in self.groups:
            if not group:
                return {}

            r = {}
            try:
                for field in self.groups:
                    if not field.listed:
                        value = field.parse_value(
                            handler.get_argument(field.name, None)
                        )
                    else:
                        value = field.parse_value(
                            handler.get_arguments(field.name)
                        )
                    if value is not None:
                        r[field.name] = value
            except exc.CommonError:
                if len(self.groups) <= 1:
                    raise
            else:
                return r
        raise exc.InputError(exc.Code.INPUT_GROUP_ERROR)


def define_arguments(*argdefs):

    def _wrapper(func):

    return _wrapper


def validate(validator, field, value):
    if value and not validator(value):
        raise exc.InputError(exc.Code.INPUT_ERROR, field)
    return value
