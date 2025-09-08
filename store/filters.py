import django_filters
from .models import Item


class ProductFilter(django_filters.FilterSet):
    """
    Filter set for Item model.
    """

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['name', 'category', 'vendor']
