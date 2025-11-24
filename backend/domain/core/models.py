"""
Core models and utilities for the Confectionery Catalog project.
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class PublishedQuerySet(models.QuerySet):
    """Custom QuerySet for published objects."""
    
    def published(self):
        """Return only published objects."""
        return self.filter(is_published=True)
    
    def unpublished(self):
        """Return only unpublished objects."""
        return self.filter(is_published=False)


class PublishedManager(models.Manager):
    """Custom manager for published objects."""
    
    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def unpublished(self):
        return self.get_queryset().unpublished()


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
        help_text=_('Timestamp when the object was created')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
        help_text=_('Timestamp when the object was last updated')
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class UUIDModel(models.Model):
    """
    An abstract base class model that provides a UUID primary key.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID')
    )

    class Meta:
        abstract = True


class PublishedModel(models.Model):
    """
    An abstract base class model that provides publication status.
    """
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Published'),
        help_text=_('Designates whether this object is publicly visible'),
        db_index=True,
    )

    objects = PublishedManager()

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """
    An abstract base class model that provides SEO meta fields.
    """
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Meta Title'),
        help_text=_('SEO meta title (max 255 characters)')
    )
    meta_description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('Meta Description'),
        help_text=_('SEO meta description (max 500 characters)')
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Meta Keywords'),
        help_text=_('SEO meta keywords, comma-separated')
    )

    class Meta:
        abstract = True
