"""
ViewSets for Products API.
"""
from django.core.cache import cache
from django.db.models import Count, Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from application.catalog.models import Category, Product, Topping, Wrapper

from .filters import ProductFilter
from .serializers import (
    CategorySerializer,
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ToppingSerializer,
    WrapperSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing categories.
    
    list: Get all published categories with product count
    retrieve: Get a single category by ID
    """
    queryset = Category.objects.published().annotate(
        product_count=Count('products', distinct=True)
    )
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'display_order', 'created_at']
    ordering = ['display_order', 'name']
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        """Cache category list for better performance."""
        return super().list(request, *args, **kwargs)


class ToppingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing toppings.
    
    list: Get all published toppings
    retrieve: Get a single topping by ID
    """
    queryset = Topping.objects.published()
    serializer_class = ToppingSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        """Cache topping list for better performance."""
        return super().list(request, *args, **kwargs)


class WrapperViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing wrappers.
    
    list: Get all published wrappers
    retrieve: Get a single wrapper by ID
    """
    queryset = Wrapper.objects.published()
    serializer_class = WrapperSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'material', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        """Cache wrapper list for better performance."""
        return super().list(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    
    list: Get all published products with filters
    retrieve: Get a single product by slug
    create: Create a new product (admin only)
    update: Update a product (admin only)
    partial_update: Partially update a product (admin only)
    destroy: Delete a product (admin only)
    
    Additional actions:
    - featured: Get featured products
    - by_category: Get products by category slug
    """
    lookup_field = 'slug'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'short_description']
    ordering_fields = ['name', 'price', 'created_at', 'display_order']
    ordering = ['display_order', '-created_at']
    
    def get_queryset(self):
        """
        Optimize queryset with select_related and prefetch_related.
        Only show published products for non-staff users.
        """
        queryset = Product.objects.select_related(
            'category',
            'wrapper',
        ).prefetch_related(
            Prefetch('toppings', queryset=Topping.objects.published())
        )
        
        # Non-staff users can only see published products
        if not self.request.user.is_staff:
            queryset = queryset.published()
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List products with caching based on query parameters.
        """
        # Generate cache key from query params
        cache_key = f"products_list_{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        
        # Cache for 5 minutes
        cache.set(cache_key, response.data, 60 * 5)
        
        return response
    
    @method_decorator(cache_page(60 * 10))  # Cache for 10 minutes
    def retrieve(self, request, *args, **kwargs):
        """Cache individual product details."""
        return super().retrieve(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Clear cache when creating a product."""
        serializer.save()
        self._clear_product_cache()
    
    def perform_update(self, serializer):
        """Clear cache when updating a product."""
        serializer.save()
        self._clear_product_cache()
    
    def perform_destroy(self, instance):
        """Clear cache when deleting a product."""
        super().perform_destroy(instance)
        self._clear_product_cache()
    
    def _clear_product_cache(self):
        """Clear all product-related cache."""
        cache.delete_pattern('products_*')
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured products.
        
        Returns products marked as featured.
        """
        queryset = self.get_queryset().filter(is_featured=True)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='category/(?P<category_slug>[^/.]+)')
    def by_category(self, request, category_slug=None):
        """
        Get products by category slug.
        
        Returns all products in the specified category.
        """
        try:
            category = Category.objects.published().get(slug=category_slug)
        except Category.DoesNotExist:
            return Response(
                {'detail': 'Category not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        queryset = self.get_queryset().filter(category=category)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
