from django import template
from django.forms.widgets import ClearableFileInput

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag('parts/bs_form_input.html')
def form_input(field):
    if type(field.field.widget) == ClearableFileInput:
        return {'field': field, 'bs_class': 'form-control-file'}
    else:
        return {'field': field, 'bs_class': 'form-control'}
