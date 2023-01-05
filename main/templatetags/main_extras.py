from django import template
register = template.Library()

@register.filter(name="comma_to_whitespace")
def comma_to_whitespace(value):
    return value.replace(","," ")