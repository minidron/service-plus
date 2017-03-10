from django.db import models

from django_fsm import FSMField, transition

from model_utils.models import TimeStampedModel

__all__ = (
    'Booking',
)


class State(object):
    """
    Содержит статусы заявки
    """
    CLIENT_ABORT = 'client_abort'
    FOR_PAYMENT = 'for_payment'
    PAYED = 'payed'
    WAITING_FOR_APPROVAL = 'waiting_for_approval'
    WAITING_FOR_PARTS = 'waiting_for_parts'
    WITHOUT_REPAIR = 'without_repair'
    WORKING = 'working'

    CHOICES = (
        (CLIENT_ABORT, 'отказ клиента'),
        (FOR_PAYMENT, 'на оплату'),
        (PAYED, 'оплачено клиентом'),
        (WAITING_FOR_APPROVAL, 'ждем подтверждения клиента'),
        (WAITING_FOR_PARTS, 'ждем запчасти'),
        (WITHOUT_REPAIR, 'без ремонта'),
        (WORKING, 'в работе'),
    )


class Booking(TimeStampedModel):
    """
    Клиентская заявка
    """
    state = FSMField(
        'статус',
        default=State.WORKING, choices=State.CHOICES, protected=True)

    client = models.ForeignKey(
        'crm.Client',
        verbose_name='клиент',
        blank=True, null=True)

    client_name = models.CharField(
        'ФИО',
        help_text='Фамилия Имя Отчество',
        max_length=254)

    client_address = models.CharField(
        'адрес',
        blank=True, max_length=254)

    client_characteristic = models.CharField(
        'характеристика/внешний вид',
        blank=True, max_length=254)

    client_email = models.EmailField(
        'email',
        blank=True)

    client_phone = models.CharField(
        'телефон',
        blank=True, max_length=254)

    imei = models.CharField(
        'IMEI',
        blank=True, max_length=30)

    brand = models.ForeignKey(
        'crm.Brand',
        verbose_name='бренд',
        blank=True, null=True)

    model = models.ForeignKey(
        'crm.Model',
        verbose_name='модель',
        blank=True, null=True)

    has_device = models.BooleanField(
        'устройство',
        default=True)

    has_battery = models.BooleanField(
        'аккумулятор',
        default=True)

    has_charger = models.BooleanField(
        'зарядное устройство',
        default=False)

    has_memory_card = models.BooleanField(
        'карта памяти',
        default=False)

    has_sim = models.BooleanField(
        'SIM-карта',
        default=False)

    has_bag_cover = models.BooleanField(
        'сумка/чехол',
        default=False)

    additional_kit = models.CharField(
        'дополнительно',
        blank=True, max_length=254)

    problem = models.TextField(
        'неисправность')

    note = models.CharField(
        'примечание',
        blank=True, max_length=254)

    estimated_date = models.DateField(
        'предполагаемая дата готовности')

    ready_date = models.DateTimeField(
        'дата готовности',
        blank=True, null=True, editable=False)

    close_date = models.DateTimeField(
        'дата выдачи',
        blank=True, null=True, editable=False)

    is_urgently = models.BooleanField(
        'срочно',
        default=False)

    estimated_cost = models.IntegerField(
        'предполагаемая стоимость')

    class Meta:
        default_related_name = 'bookings'
        ordering = ['-pk']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return str(self.pk)

    @transition(field=state, source=State.WORKING,
                target=State.WAITING_FOR_APPROVAL)
    def wait_agree(self):
        """
        Согласовать детали ремонта
        """

    @transition(field=state, source=State.WORKING,
                target=State.WAITING_FOR_PARTS)
    def wait_parts(self):
        """
        Ждать запчасти
        """

    @transition(field=state, source=State.WORKING, target=State.WITHOUT_REPAIR)
    def reject(self):
        """
        Ремонт не требуется или невозможен
        """

    @transition(field=state, source=State.WORKING, target=State.FOR_PAYMENT)
    def ready(self):
        """
        Готов к выдачи
        """

    @transition(field=state, source=[State.FOR_PAYMENT, State.WITHOUT_REPAIR],
                target=State.PAYED)
    def close(self):
        """
        Закрыть заявку
        """

    def can_repair(self):
        return self.state != 'working'

    @transition(field=state, source='*', target=State.WORKING,
                conditions=[can_repair])
    def repair(self):
        """
        Вернуть в ремонт
        """

    @property
    def kit(self):
        """
        Полная комплектация
        """
        device = 'устройство' if self.has_device else None
        battery = 'аккумулятор' if self.has_battery else None
        charger = 'зарядное устройство' if self.has_charger else None
        memory_card = 'карта памяти' if self.has_memory_card else None
        sim = 'SIM-карта' if self.has_sim else None
        bag_cover = 'сумка/чехол' if self.has_bag_cover else None
        return ', '.join(filter(None, [device, battery, charger, memory_card,
                                       sim, bag_cover, self.additional_kit]))

    @property
    def available_transitions(self):
        """
        Доступные статусы
        """
        return [tr.name for tr in self.get_available_state_transitions()]
