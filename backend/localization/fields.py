from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from localization.helpers import get_language_from_request
from django.db.models.fields.files import FileField, FieldFile

class TranslatedField(serializers.CharField):
    """
    Translated field
    """

    def __init__(self, field_name, *args, **kwargs):
        self.field_name = field_name
        kwargs["source"] = "*"
        super().__init__(*args, **kwargs)

    def to_representation(self, obj):
        request = self.context.get("request")

        if not request:
            raise ValueError("Request non presente nel contesto del serializer")
        
        lang = get_language_from_request(request)

        try:
            translation = obj.translations.get(lang=lang)
            value = getattr(translation, self.field_name)
        except ObjectDoesNotExist:
            return None

        if value is None:
            return None
        
        return value