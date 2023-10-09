from django import template
from django.utils.text import capfirst

register = template.Library()


@register.filter(name="snake_to_user_readable")
def snake_to_user_readable(value: str):
    value = value.replace("avg", "Average")
    words = value.split("_")
    return words[0].capitalize() + " " + " ".join(word.lower() for word in words[1:])


@register.filter(name="getattr")
def get_attribute(obj, attr_name):
    return obj.get(attr_name)
