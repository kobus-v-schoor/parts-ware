from django import template
from django.forms.widgets import ClearableFileInput

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag('parts/bs_form_input.html')
def form_input(field):
    context = {'field': field}

    if type(field.field.widget) == ClearableFileInput:
        context['bs_class'] = 'form-control-file'
    else:
        context['bs_class'] = 'form-control'

    if field.errors:
        context['bs_class'] += ' is-invalid'

    return context
