"""
Filters for Products API.
"""
from django_filters import rest_framework as filters

from application.catalog.models import Product


class ProductFilter(filters.FilterSet):
    """Filter set for Product model."""
    
    # Price range filters
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Weight range filters
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    
    # Calorie range filters
    min_calories = filters.NumberFilter(field_name='calories', lookup_expr='gte')
    max_calories = filters.NumberFilter(field_name='calories', lookup_expr='lte')
    
    # Category filter
    category = filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    
    # Featured filter
    is_featured = filters.BooleanFilter(field_name='is_featured')
    
    # Stock filter
    in_stock = filters.BooleanFilter(field_name='in_stock')
    
    # Topping filter
    toppings = filters.CharFilter(field_name='toppings__slug', lookup_expr='exact')
    
    class Meta:
        model = Product
        fields = [
            'category',
            'is_featured',
            'in_stock',
            'min_price',
            'max_price',
            'min_weight',
            'max_weight',
            'min_calories',
            'max_calories',
            'toppings',
        ]
