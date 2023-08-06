from enum import Enum


class FieldType(Enum):
    TEXT = 'text'
    PASSWORD = 'password'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    NUMBER = 'number'
    RANGE = 'range'
    COLOR = 'color'
    DATE = 'date'
    TIME = 'time'
    EMAIL = 'email'
    URL = 'url'
    SEARCH = 'search'
    FILE = 'file'
    IMAGE = 'image'
    RESET = 'reset'
    SUBMIT = 'submit'
    BUTTON = 'button'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class FieldValidation(Enum):
    REQUIRED = 'required'
    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'
    MIN_VALUE = 'min_value'
    MAX_VALUE = 'max_value'
    PATTERN = 'pattern'
    STEP = 'step'
    ACCEPTED_TYPES = 'accepted_types'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)