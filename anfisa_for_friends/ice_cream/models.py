from django.db import models
from core.models import PublishedModel


class Category(PublishedModel):
    """
    Модель для категорий мороженого.
    Наследуется от PublishedModel, добавляющей флаг is_published.
    """
    title = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Слаг')
    output_order = models.PositiveSmallIntegerField(
        default=100, verbose_name='Порядок вывода'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Topping(PublishedModel):
    """
    Модель для топпингов мороженого.
    Наследуется от PublishedModel, добавляющей флаг is_published.
    """
    title = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=64, unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'


class Wrapper(PublishedModel):
    """
    Модель для оберток мороженого.
    Наследуется от PublishedModel, добавляющей флаг is_published.
    """
    title = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обертка'
        verbose_name_plural = 'Обертки'


class IceCream(PublishedModel):
    """
    Модель для мороженого.
    Наследуется от PublishedModel, добавляющей флаг is_published.
    """
    title = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    wrapper = models.OneToOneField(
        Wrapper,
        on_delete=models.SET_NULL,
        related_name='ice_cream',
        null=True,
        blank=True,
        verbose_name='Обертка'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='ice_creams',
        verbose_name='Категория'
    )
    toppings = models.ManyToManyField(Topping, verbose_name='Топпинги')
    is_on_main = models.BooleanField(default=False, verbose_name='На главной')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Мороженое'
        verbose_name_plural = 'Мороженое'
