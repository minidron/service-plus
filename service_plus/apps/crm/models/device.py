from django.db import models

__all__ = (
    'Brand',
    'Model',
)


class Brand(models.Model):
    """
    Торговая марка устройства
    """
    name = models.CharField(
        'название',
        max_length=254, db_index=True)

    class Meta:
        ordering = ['-name']
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'

    def __str__(self):
        return self.name


class Model(models.Model):
    """
    Модель устройства
    """
    name = models.CharField(
        'название',
        max_length=254, db_index=True)

    brand = models.ForeignKey(
        'crm.Brand',
        verbose_name='бренд')

    class Meta:
        ordering = ['-name']
        verbose_name = 'модель'
        verbose_name_plural = 'модели'

    def __str__(self):
        return self.name
