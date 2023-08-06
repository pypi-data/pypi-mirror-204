from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .consts import Type
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "email",
            "description",
            "type",
        )

    def validate_type(self, value):
        TYPE_CHOICES_PATH = getattr(settings, "TYPE_CHOICES_PATH", None)

        if TYPE_CHOICES_PATH:
            try:
                types = import_string(TYPE_CHOICES_PATH)
            except ImportError:
                raise ImproperlyConfigured("module cannot be resolved.")
        else:
            types = Type

        try:
            return types(value)
        except ValueError:
            raise ValidationError({"type": "invalid choice"})
