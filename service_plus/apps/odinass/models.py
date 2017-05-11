import uuid

from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(
        'название', max_length=254)

    parent = TreeForeignKey(
        'self',
        verbose_name='родительская категория',
        related_name='children',
        null=True, blank=True, db_index=True)

    class Meta:
        default_related_name = 'categories'
        ordering = ['title']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title
