from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag('parts/bs_form_input.html')
def form_input(field):
    return {'field': field}
