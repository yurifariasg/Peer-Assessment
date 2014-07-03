from django import template
register = template.Library()

@register.filter(name='access')
def access(value, arg):
    return value[arg]

@register.filter(name='getattribute')
def getattribute(value, arg):
    return getattr(value, arg)
