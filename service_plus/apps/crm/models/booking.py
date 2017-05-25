from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.functions import Now

from dateutil.relativedelta import relativedelta

from django_fsm import FSMField, transition

from model_utils.models import TimeStampedModel

__all__ = (
    'Booking',
    'Guarantee',
    'State',
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


class Guarantee(models.Model):
    """
    Гарантия по заявке
    """
    title = models.CharField(
        'название',
        max_length=254, db_index=True)

    day = models.PositiveSmallIntegerField(
        'дней',
        blank=True, null=True)

    month = models.PositiveSmallIntegerField(
        'месяцев',
        blank=True, null=True)

    year = models.PositiveSmallIntegerField(
        'лет',
        blank=True, null=True)

    order = models.PositiveIntegerField(
        u'порядок',
        default=0)

    class Meta:
        default_related_name = 'guarantees'
        ordering = ['order']
        verbose_name = 'гарантия'
        verbose_name_plural = 'гарантии'

    def __str__(self):
        return self.title

    @property
    def relative_data(self):
        """
        Промежуток времени, когда длится гарантия
        """
        return relativedelta(day=self.day, month=self.month, year=self.year)


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
        on_delete=models.SET_NULL,
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
        on_delete=models.SET_NULL,
        blank=True, null=True)

    model = models.ForeignKey(
        'crm.Model',
        verbose_name='модель',
        on_delete=models.SET_NULL,
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

    done_work = JSONField(
        'выполненная работа',
        blank=True, null=True)

    guarantee = models.ForeignKey(
        'crm.Guarantee',
        verbose_name='гарантия',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    master = models.ForeignKey(
        'auth.User',
        verbose_name='мастер',
        on_delete=models.SET_NULL,
        limit_choices_to={'groups__name': 'Мастер'},
        blank=True, null=True)

    spare_parts = models.ManyToManyField(
        'crm.SparePart',
        verbose_name='запчасти',
        through='SparePartCount')

    gain = models.PositiveIntegerField(
        'полученные деньги',
        default=0, blank=True, null=True)

    replacement_device = models.OneToOneField(
        'crm.ReplacementDevice',
        verbose_name='устройство на замену',
        on_delete=models.SET_NULL,
        blank=True, null=True)

    class Meta:
        default_related_name = 'bookings'
        ordering = ['-pk']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return str(self.pk)

    @transition(field=state, source=State.WORKING,
                target=State.WAITING_FOR_APPROVAL)
    def wait_agree(self, user=None):
        """
        Согласовать детали ремонта
        """

    @transition(field=state, source=State.WORKING,
                target=State.WAITING_FOR_PARTS)
    def wait_parts(self, user=None):
        """
        Ждать запчасти
        """

    @transition(field=state, source=State.WORKING, target=State.WITHOUT_REPAIR)
    def reject(self, user=None):
        """
        Ремонт не требуется или невозможен
        """

    @transition(field=state, source=State.WORKING, target=State.FOR_PAYMENT)
    def ready(self, user=None):
        """
        Готов к выдачи
        """
        if not self.master:
            groups_name = [name for name in user.groups.values_list('name',
                                                                    flat=True)]
            if 'Мастер' in groups_name:
                self.master = user
        self.ready_date = Now()

    def can_close(self):
        replacement_device = False if self.replacement_device else True
        money = self.debt == 0
        return all([replacement_device, money])

    @transition(field=state, source=[State.FOR_PAYMENT, State.WITHOUT_REPAIR],
                target=State.PAYED, conditions=[can_close])
    def close(self, user=None):
        """
        Закрыть заявку
        """
        self.close_date = Now()

    def can_repair(self):
        return self.state != 'working'

    @transition(field=state, source='*', target=State.WORKING,
                conditions=[can_repair])
    def repair(self, user=None):
        """
        Вернуть в ремонт
        """
        self.ready_date = None
        self.close_date = None

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

    @property
    def done_work_sum(self):
        done_work_sum = 0
        if self.done_work:
            done_work_sum = sum(job['price'] for job in self.done_work)
        return done_work_sum

    @property
    def spare_part_sum(self):
        return sum(self.spare_part_counts.values_list('retail_price',
                                                      flat=True))

    @property
    def total_sum(self):
        return self.done_work_sum + self.spare_part_sum

    @property
    def debt(self):
        return self.total_sum - self.gain

    @property
    def guarantee_items(self):
        items = []
        for item in self.spare_part_counts.all():
            items.append({
                'title': item.title,
                'price': item.retail_price or '',
                'guarantee': item.guarantee or '',
            })

        for item in self.done_work:
            items.append({
                'title': item['title'],
                'price': item['price'] or '',
                'guarantee': self.guarantee or '',
            })

        return items
