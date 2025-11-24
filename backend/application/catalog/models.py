"""
Product models for the Confectionery Catalog.
"""
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from domain.core.models import PublishedModel, SEOModel, TimeStampedModel


class Category(TimeStampedModel, PublishedModel, SEOModel):
    """
    Product category model.
    Represents different categories of confectionery products.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Name'),
        help_text=_('Category name')
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_('Slug'),
        help_text=_('URL-friendly name'),
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Category description')
    )
    display_order = models.PositiveSmallIntegerField(
        default=100,
        verbose_name=_('Display Order'),
        help_text=_('Order in which categories are displayed'),
        db_index=True,
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Icon'),
        help_text=_('Icon class name (e.g., for Font Awesome)')
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['display_order', 'is_published']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Topping(TimeStampedModel, PublishedModel):
    """
    Topping model for confectionery products.
    Represents various toppings that can be added to products.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Name'),
        help_text=_('Topping name')
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_('Slug'),
        help_text=_('URL-friendly name'),
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Topping description')
    )

    class Meta:
        verbose_name = _('Topping')
        verbose_name_plural = _('Toppings')
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Wrapper(TimeStampedModel, PublishedModel):
    """
    Wrapper model for confectionery products.
    Represents different wrapper types for products.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Name'),
        help_text=_('Wrapper name')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Wrapper description')
    )
    material = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Material'),
        help_text=_('Wrapper material type')
    )
    is_recyclable = models.BooleanField(
        default=False,
        verbose_name=_('Recyclable'),
        help_text=_('Is the wrapper recyclable?')
    )

    class Meta:
        verbose_name = _('Wrapper')
        verbose_name_plural = _('Wrappers')
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_published']),
            models.Index(fields=['is_recyclable']),
        ]

    def __str__(self):
        return self.name


class Product(TimeStampedModel, PublishedModel, SEOModel):
    """
    Main product model for confectionery items.
    Represents individual confectionery products with all their attributes.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Product name'),
        db_index=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_('Slug'),
        help_text=_('URL-friendly name'),
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('Detailed product description')
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_('Short Description'),
        help_text=_('Brief product description for listings')
    )
    
    # Relationships
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('Category'),
        help_text=_('Product category'),
        db_index=True,
    )
    wrapper = models.OneToOneField(
        Wrapper,
        on_delete=models.SET_NULL,
        related_name='product',
        null=True,
        blank=True,
        verbose_name=_('Wrapper'),
        help_text=_('Product wrapper type')
    )
    toppings = models.ManyToManyField(
        Topping,
        related_name='products',
        blank=True,
        verbose_name=_('Toppings'),
        help_text=_('Available toppings for this product')
    )
    
    # Product attributes
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Price'),
        help_text=_('Product price'),
        db_index=True,
    )
    weight = models.PositiveIntegerField(
        verbose_name=_('Weight (grams)'),
        help_text=_('Product weight in grams'),
        null=True,
        blank=True,
    )
    calories = models.PositiveIntegerField(
        verbose_name=_('Calories'),
        help_text=_('Calories per 100g'),
        null=True,
        blank=True,
    )
    
    # Display settings
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('Featured'),
        help_text=_('Display on homepage'),
        db_index=True,
    )
    display_order = models.PositiveSmallIntegerField(
        default=100,
        verbose_name=_('Display Order'),
        help_text=_('Order in which products are displayed'),
    )
    
    # Inventory
    in_stock = models.BooleanField(
        default=True,
        verbose_name=_('In Stock'),
        help_text=_('Is the product available for purchase?'),
        db_index=True,
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Stock Quantity'),
        help_text=_('Available quantity in stock')
    )
    
    # Media
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('Image'),
        help_text=_('Product image')
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['is_featured', 'is_published']),
            models.Index(fields=['price']),
            models.Index(fields=['display_order', '-created_at']),
            models.Index(fields=['in_stock', 'is_published']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        """Check if product is available for purchase."""
        return self.is_published and self.in_stock and self.stock_quantity > 0
