from django.db import models


class PublishedModel(models.Model):
    """
    Абстрактная модель, добавляющая флаг is_published.

    Поля:
    is_published -- флаг, указывающий, опубликован ли объект (по умолчанию True)
    """
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    class Meta:
        abstract = True
        verbose_name = 'Опубликованная модель'
        verbose_name_plural = 'Опубликованные модели'
