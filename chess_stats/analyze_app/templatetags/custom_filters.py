from django import template
from django.utils.text import capfirst

register = template.Library()


@register.filter(name="snake_to_user_readable")
def snake_to_user_readable(value):
    words = value.split("_")
    return words[0].capitalize() + " " + " ".join(word.lower() for word in words[1:])
