from django.utils.text import slugify as django_slugify

def custom_slugify(value):
    """
    Cria um slug que substitui '@' e '.' por hífens antes de slugificar.
    """
    value = value.replace('@', '-').replace('.', '-').replace('_', '-')
    return django_slugify(value)