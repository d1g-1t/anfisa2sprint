from django.contrib import admin
from .models import Category, Topping, Wrapper, IceCream


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для модели Category.

    Отображает поля title, slug, output_order и is_published.
    Позволяет искать по полям title и slug.
    Фильтрация по полю is_published.
    Сортировка по полю output_order.
    """
    list_display = ('title', 'slug', 'output_order', 'is_published')
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)
    ordering = ('output_order',)


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    """
    Админка для модели Topping.

    Отображает поля title, slug и is_published.
    Позволяет искать по полям title и slug.
    Фильтрация по полю is_published.
    """
    list_display = ('title', 'slug', 'is_published')
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)


@admin.register(Wrapper)
class WrapperAdmin(admin.ModelAdmin):
    """
    Админка для модели Wrapper.

    Отображает поля title и is_published.
    Позволяет искать по полю title.
    Фильтрация по полю is_published.
    """
    list_display = ('title', 'is_published')
    search_fields = ('title',)
    list_filter = ('is_published',)


@admin.register(IceCream)
class IceCreamAdmin(admin.ModelAdmin):
    """
    Админка для модели IceCream.

    Отображает поля title, category, is_on_main и is_published.
    Позволяет искать по полям title и description.
    Фильтрация по полям is_published, is_on_main и category.
    Использует горизонтальный фильтр для поля toppings.
    Использует raw_id_fields для поля wrapper.
    """
    list_display = ('title', 'category', 'is_on_main', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('is_published', 'is_on_main', 'category')
    filter_horizontal = ('toppings',)
    raw_id_fields = ('wrapper',)