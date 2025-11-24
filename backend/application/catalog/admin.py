"""
Admin configuration for Products application.
"""
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Category, Product, Topping, Wrapper


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = (
        'name',
        'slug',
        'display_order',
        'product_count',
        'is_published',
        'created_at',
    )
    list_filter = ('is_published', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        (_('Display Settings'), {
            'fields': ('display_order', 'is_published')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with annotations."""
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _product_count=Count('products', distinct=True)
        )
    
    @admin.display(description=_('Products'))
    def product_count(self, obj):
        """Display count of products in category."""
        return obj._product_count


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    """Admin configuration for Topping model."""
    
    list_display = (
        'name',
        'slug',
        'product_count',
        'is_published',
        'created_at',
    )
    list_filter = ('is_published', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """Optimize queryset with annotations."""
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _product_count=Count('products', distinct=True)
        )
    
    @admin.display(description=_('Products'))
    def product_count(self, obj):
        """Display count of products using this topping."""
        return obj._product_count


@admin.register(Wrapper)
class WrapperAdmin(admin.ModelAdmin):
    """Admin configuration for Wrapper model."""
    
    list_display = (
        'name',
        'material',
        'is_recyclable',
        'has_product',
        'is_published',
        'created_at',
    )
    list_filter = ('is_recyclable', 'is_published', 'created_at')
    search_fields = ('name', 'material', 'description')
    ordering = ('name',)
    date_hierarchy = 'created_at'
    
    @admin.display(description=_('In Use'), boolean=True)
    def has_product(self, obj):
        """Check if wrapper is assigned to a product."""
        return hasattr(obj, 'product') and obj.product is not None


class ToppingInline(admin.TabularInline):
    """Inline for managing product toppings."""
    model = Product.toppings.through
    extra = 1
    verbose_name = _('Topping')
    verbose_name_plural = _('Toppings')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    
    list_display = (
        'name',
        'category',
        'formatted_price',
        'stock_status',
        'is_featured',
        'is_published',
        'display_order',
        'created_at',
    )
    list_filter = (
        'is_published',
        'is_featured',
        'in_stock',
        'category',
        'created_at',
    )
    search_fields = (
        'name',
        'slug',
        'description',
        'short_description',
    )
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', '-created_at')
    date_hierarchy = 'created_at'
    filter_horizontal = ('toppings',)
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'name',
                'slug',
                'category',
                'short_description',
                'description',
                'image',
            )
        }),
        (_('Pricing & Attributes'), {
            'fields': (
                'price',
                'weight',
                'calories',
            )
        }),
        (_('Relations'), {
            'fields': (
                'wrapper',
                'toppings',
            )
        }),
        (_('Inventory'), {
            'fields': (
                'in_stock',
                'stock_quantity',
            )
        }),
        (_('Display Settings'), {
            'fields': (
                'is_featured',
                'display_order',
                'is_published',
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        queryset = super().get_queryset(request)
        return queryset.select_related('category', 'wrapper').prefetch_related('toppings')
    
    @admin.display(description=_('Price'))
    def formatted_price(self, obj):
        """Display formatted price."""
        return f'${obj.price:.2f}'
    
    @admin.display(description=_('Stock'))
    def stock_status(self, obj):
        """Display stock status with color coding."""
        if not obj.in_stock:
            color = 'red'
            text = _('Out of Stock')
        elif obj.stock_quantity == 0:
            color = 'red'
            text = _('No Stock')
        elif obj.stock_quantity < 10:
            color = 'orange'
            text = f'{obj.stock_quantity} {_("units")}'
        else:
            color = 'green'
            text = f'{obj.stock_quantity} {_("units")}'
        
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            text
        )
    
    actions = ['mark_as_published', 'mark_as_unpublished', 'mark_as_featured']
    
    @admin.action(description=_('Mark selected products as published'))
    def mark_as_published(self, request, queryset):
        """Mark selected products as published."""
        updated = queryset.update(is_published=True)
        self.message_user(request, _(f'{updated} products marked as published.'))
    
    @admin.action(description=_('Mark selected products as unpublished'))
    def mark_as_unpublished(self, request, queryset):
        """Mark selected products as unpublished."""
        updated = queryset.update(is_published=False)
        self.message_user(request, _(f'{updated} products marked as unpublished.'))
    
    @admin.action(description=_('Mark selected products as featured'))
    def mark_as_featured(self, request, queryset):
        """Mark selected products as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(request, _(f'{updated} products marked as featured.'))
