import re

from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Container, Part

class ContainerForm(ModelForm):
    class Meta:
        model = Container
        fields = ['name', 'description', 'naming_scheme']

    def clean_naming_scheme(self):
        ns = self.cleaned_data['naming_scheme']

        # check if naming scheme is valid regex
        try:
            re.compile(ns)
            valid = True
        except re.error:
            valid = False

        if not valid:
            raise ValidationError("Naming scheme is not a valid regex")

        return ns
