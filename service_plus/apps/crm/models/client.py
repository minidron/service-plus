from django.db import models

from model_utils.models import TimeStampedModel

__all__ = (
    'Client',
)


class Client(TimeStampedModel):
    """
    Клиент
    """
    name = models.CharField(
        'имя',
        max_length=254)

    surname = models.CharField(
        'фамилия',
        max_length=254)

    patronymic = models.CharField(
        'отчество',
        blank=True, max_length=254)

    address = models.CharField(
        'адрес',
        blank=True, max_length=254)

    characteristic = models.CharField(
        'характеристика',
        blank=True, max_length=254)

    email = models.EmailField(
        'email',
        blank=True)

    phone = models.CharField(
        'телефон',
        blank=True, max_length=254)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['surname', 'name', 'patronymic']

    def __str__(self):
        name = '%s.' % self.name[0]
        patronymic = self.patronymic
        if patronymic:
            patronymic = patronymic[0]
        name = '%s.' % self.name[0]
        return ' '.join(filter(None, [self.surname, name, patronymic]))
