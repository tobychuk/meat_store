from django.db import models
from datetime import datetime
# Create your models here.

class Client(models.Model):
    first_name = models.CharField('Имя', max_length=15)
    last_name = models.CharField("Фамилия", max_length=15)
    middle_name = models.CharField("Отчество", max_length=15, blank=True, null=True, help_text='Необязательное поле')
    phone_number = models.IntegerField("Телефонный номер")
    reserve_phone_number = models.IntegerField("Запасной телефонный номер", blank=True, null=True, help_text='Необязательное поле')
    address = models.CharField("Адрес проживания", max_length=100)
    passport_image_first = models.ImageField("Фото лицевой стороны паспорта", upload_to='documents/')
    passport_image_second = models.ImageField("Фото задней стороны паспорта", upload_to='documents/')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Debt(models.Model):
    STATUS_PAID = 'paid'
    STATUS_NOT_PAID = 'not paid'
    DEBT_STATUSES = (
        (STATUS_NOT_PAID, 'Не оплачен',),
        (STATUS_PAID, 'Оплачен',),
    )
    debtor = models.ForeignKey(Client, verbose_name='Должник', on_delete=models.CASCADE, related_name='debts')
    quantity = models.IntegerField("Размер долга")
    amount_meat = models.SmallIntegerField("Количество мяса")
    status = models.CharField('Статус', max_length=40, choices=DEBT_STATUSES, default=STATUS_NOT_PAID)
    expired = models.BooleanField('Просрочен?', default=False)
    created = models.DateField("Дата выдачи")
    return_date = models.DateField("Дата возврата", blank=True, null=True)
    updated = models.DateField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'

    def __str__(self):
        return f"{self.debtor} - {self.quantity}"

class Log(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, related_name='logs')
    text = models.TextField("Действие")
    created = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering=['created']

    def __str__(self):
        return self.text