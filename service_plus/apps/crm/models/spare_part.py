from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


__all__ = (
    'SparePart',
    'SparePartCount',
)


class SparePartCount(models.Model):
    """
    Кол-во одного типа запчастей
    """
    booking = models.ForeignKey(
        'crm.Booking',
        verbose_name='заявка',
        on_delete=models.CASCADE,
        blank=True, null=True, editable=False)

    spare_part = models.ForeignKey(
        'crm.SparePart',
        verbose_name='запчасть',
        on_delete=models.SET_NULL,
        blank=True, null=True, editable=False)

    title = models.CharField(
        'название',
        max_length=254)

    brand = models.ForeignKey(
        'crm.Brand',
        verbose_name='бренд',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    model = models.ForeignKey(
        'crm.Model',
        verbose_name='модель',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    purchase_price = models.PositiveIntegerField(
        'цена закупки',
        default=0)

    retail_price = models.PositiveIntegerField(
        'цена розницы',
        default=0)

    class Meta:
        default_related_name = 'spare_part_counts'
        verbose_name = 'колличество запчастей'
        verbose_name_plural = 'колличества запчастей'

    def save(self, *args, **kwargs):
        self.set_fields()
        super().save(*args, **kwargs)

    def set_fields(self):
        if self.spare_part:
            self.title = self.spare_part.title
            self.brand = self.spare_part.brand
            self.model = self.spare_part.model
            self.purchase_price = self.spare_part.purchase_price
            self.retail_price = self.spare_part.retail_price


class SparePart(models.Model):
    """
    Запчасть
    """
    title = models.CharField(
        'название',
        max_length=254)

    brand = models.ForeignKey(
        'crm.Brand',
        verbose_name='бренд',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    model = models.ForeignKey(
        'crm.Model',
        verbose_name='модель',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    purchase_price = models.PositiveIntegerField(
        'цена закупки',
        default=0)

    retail_price = models.PositiveIntegerField(
        'цена розницы',
        default=0)

    class Meta:
        default_related_name = 'spare_parts'
        ordering = ['title']
        verbose_name = 'запчасть'
        verbose_name_plural = 'запчасти'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        count = kwargs.pop('count', None)
        super().save(*args, **kwargs)
        post_save.send(sender=self.__class__, instance=self, created=True,
                       count=count)


@receiver(pre_save, sender=SparePart)
def delete_spare_part_counts(sender, instance, **kwargs):
    instance.spare_part_counts.exclude(booking__isnull=False).delete()


@receiver(post_save, sender=SparePart)
def create_spare_part_counts(sender, instance, created, count=None, **kwargs):
    if count:
        obj = SparePartCount(spare_part=instance, title=instance.title,
                             brand=instance.brand, model=instance.model,
                             purchase_price=instance.purchase_price,
                             retail_price=instance.retail_price)
        spare_part_counts = [obj for i in range(count)]
        SparePartCount.objects.bulk_create(spare_part_counts)


@receiver(pre_delete, sender=SparePart)
def delete_spare_part_counts_after_delete_spare_part(sender, instance, **kwargs):  # NOQA
    instance.spare_part_counts.exclude(booking__isnull=False).delete()
