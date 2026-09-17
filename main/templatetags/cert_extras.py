from django import template

register = template.Library()


@register.filter
def first_space_br(value):
    """Заменяет первый пробел на перенос строки."""
    return value.replace(' ', '\n', 1)