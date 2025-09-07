import django_filters
from .models import Item

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Busca parcial case-insensitive

    class Meta:
        model = Item
        fields = ['name', 'category', 'vendor']

