from django.db import models

__all__ = (
    'Brand',
    'Model',
    'ReplacementDevice',
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


class ReplacementDevice(models.Model):
    """
    Устройство на замену
    """
    name = models.CharField(
        'название',
        max_length=254, db_index=True, editable=False)

    brand = models.ForeignKey(
        'crm.Brand',
        verbose_name='бренд')

    model = models.ForeignKey(
        'crm.Model',
        verbose_name='модель')

    imei = models.CharField(
        'IMEI/SN',
        blank=True, max_length=30)

    description = models.TextField(
        'описание',
        blank=True)

    class Meta:
        ordering = ['-name']
        verbose_name = 'устройство на замену'
        verbose_name_plural = 'устройства на замену'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = '%s %s' % (self.brand, self.model)
        super().save(*args, **kwargs)
