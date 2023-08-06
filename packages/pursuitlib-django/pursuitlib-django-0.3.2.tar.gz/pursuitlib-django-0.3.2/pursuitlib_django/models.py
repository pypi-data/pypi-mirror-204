from typing import TypeVar, Type, Optional, Union

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields import Field
from django.db.models.fields.files import FileField, ImageField
from django.forms import forms
from pursuitlib.indexedenum import IndexedEnum
from pursuitlib.utils import is_null_or_empty

# Read the Django configuration
MAX_UPLOAD_SIZE = getattr(settings, "MAX_UPLOAD_SIZE", 5)  # The default max upload size is 5 MiB


MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE * 1024 * 1024  # Convert from MiB to bytes
UPLOAD_ERROR_MSG = f"Le fichier téléversé est trop grand. Il doit avoir une taille inférieure à {MAX_UPLOAD_SIZE} Mo"


T = TypeVar("T", bound=IndexedEnum)


class EnumField(Field):
    @staticmethod
    def get_choices_for(enum: Type[T]):
        return [(item, str(item.value)) for item in enum]

    def __init__(self, enum: Type[T], **kwargs):
        super().__init__(choices=EnumField.get_choices_for(enum), **kwargs)
        self.enum = enum

    def get_internal_type(self):
        return "IntegerField"

    # Create a DB value from an enum.
    # Integers are also accepted as they're easier to use in migration files
    def get_prep_value(self, value: Union[T, int]):
        if is_null_or_empty(value):
            return None
        if isinstance(value, int):
            value = self.get_at(value)
        return super().get_prep_value(value.ordinal)

    # Create an enum from a DB value
    def from_db_value(self, value, expression, connection) -> Optional[T]:
        if value is None:
            return None
        return self.get_at(int(value))

    # Try to get an enum from another value
    def to_python(self, value) -> Optional[T]:
        if is_null_or_empty(value):
            return None
        if isinstance(value, self.enum):
            return value

        try:
            return self.enum[value]
        except KeyError:
            raise ValidationError("Invalid enum value")

    def deconstruct(self):
        name, path, lst, keywords = super().deconstruct()

        # Choices are handled by the "enum" parameter
        del keywords["choices"]
        keywords["enum"] = self.enum

        return name, path, lst, keywords

    def get_at(self, index: int) -> T:
        # Clamp the index to avoid raising errors
        length = len(self.enum)
        index = max(0, min(index, length - 1))
        return self.enum.values()[index]


class FileUploadField(FileField):
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        if data.file.size > MAX_UPLOAD_SIZE_BYTES:
            raise forms.ValidationError(UPLOAD_ERROR_MSG)
        return data


class ImageUploadField(ImageField):
    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)
        if data.file.size > MAX_UPLOAD_SIZE_BYTES:
            raise forms.ValidationError(UPLOAD_ERROR_MSG)
        return data
