"""
Serializers for Products API.
"""
from rest_framework import serializers

from application.catalog.models import Category, Product, Topping, Wrapper


class ToppingSerializer(serializers.ModelSerializer):
    """Serializer for Topping model."""
    
    class Meta:
        model = Topping
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class WrapperSerializer(serializers.ModelSerializer):
    """Serializer for Wrapper model."""
    
    class Meta:
        model = Wrapper
        fields = (
            'id',
            'name',
            'description',
            'material',
            'is_recyclable',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    product_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'display_order',
            'icon',
            'product_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'product_count', 'created_at', 'updated_at')


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for Product list view (optimized with minimal data)."""
    
    category = serializers.StringRelatedField()
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'short_description',
            'category',
            'category_slug',
            'price',
            'weight',
            'calories',
            'is_featured',
            'in_stock',
            'is_available',
            'image',
            'created_at',
        )
        read_only_fields = fields


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product detail view (with full relations)."""
    
    category = CategorySerializer(read_only=True)
    wrapper = WrapperSerializer(read_only=True)
    toppings = ToppingSerializer(many=True, read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    # Write-only fields for creating/updating
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.published(),
        source='category',
        write_only=True,
        required=False,
    )
    wrapper_id = serializers.PrimaryKeyRelatedField(
        queryset=Wrapper.objects.published(),
        source='wrapper',
        write_only=True,
        required=False,
        allow_null=True,
    )
    topping_ids = serializers.PrimaryKeyRelatedField(
        queryset=Topping.objects.published(),
        source='toppings',
        many=True,
        write_only=True,
        required=False,
    )
    
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'short_description',
            'category',
            'category_id',
            'wrapper',
            'wrapper_id',
            'toppings',
            'topping_ids',
            'price',
            'weight',
            'calories',
            'is_featured',
            'in_stock',
            'stock_quantity',
            'is_available',
            'display_order',
            'image',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'category',
            'wrapper',
            'toppings',
            'is_available',
            'created_at',
            'updated_at',
        )


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating products."""
    
    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'description',
            'short_description',
            'category',
            'wrapper',
            'toppings',
            'price',
            'weight',
            'calories',
            'is_featured',
            'in_stock',
            'stock_quantity',
            'display_order',
            'image',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'is_published',
        )
        
    def validate_price(self, value):
        """Ensure price is positive."""
        if value < 0:
            raise serializers.ValidationError("Price must be positive.")
        return value
    
    def validate_stock_quantity(self, value):
        """Ensure stock quantity is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
