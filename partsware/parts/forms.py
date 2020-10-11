import re

from django.forms import ModelForm, CharField, TextInput
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

class PartForm(ModelForm):
    tags = CharField(required=False, widget=TextInput(attrs={
        'placeholder':'Comma-separated tags'}))

    class Meta:
        model = Part
        fields = ['name', 'image', 'description', 'datasheet', 'pinout',
                  'quantity', 'price', 'container', 'location',]

    def clean_container(self):
        container = self.cleaned_data['container']

        if container.user != self.user:
            raise ValidationError("Container not owned by this user")

        return container

    def clean_location(self):
        location = self.cleaned_data['location']
        container = self.cleaned_data['container']

        if not re.match(f'^{container.naming_scheme}$', location):
            raise ValidationError("Location doesn't match container's "
                                  "naming scheme: %(ns)s",
                                  params={'ns': container.naming_scheme})

        return location
