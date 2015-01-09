from django import template

register = template.Library()

@register.filter(name_to_url='name_to_url')

def name_to_url(e):

    name = e.first_name + ' ' + e.last_name

    pieces = name.lower().split()

    return '-'.join(pieces)