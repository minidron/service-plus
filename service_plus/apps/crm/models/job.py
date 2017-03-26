from django.db import models

__all__ = (
    'Job',
)


class Job(models.Model):
    """
    Прейскурант работ
    """
    title = models.CharField(
        'наименование работы',
        max_length=254, db_index=True)

    price = models.IntegerField(
        'цена',
        default=0)

    class Meta:
        ordering = ['title']
        verbose_name = 'работа'
        verbose_name_plural = 'работы'

    def __str__(self):
        return self.title
