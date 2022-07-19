from django.db import models
from datetime import datetime
# Create your models here.

class Client(models.Model):
    first_name = models.CharField('Имя', max_length=15)
    last_name = models.CharField("Фамилия", max_length=15)
    middle_name = models.CharField("Отчество", max_length=15)
    phone_number = models.IntegerField("Телефонный номер")
    reserve_phone_number = models.IntegerField("Запасной телефонный номер", blank=True, null=True)
    address = models.CharField("Адрес проживания", max_length=100)
    passport_image_first = models.ImageField("Фото лицевой стороны паспорта", upload_to='documents/')
    passport_image_second = models.ImageField("Фото задней стороны паспорта", upload_to='documents/')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Debt(models.Model):
    DEBT_STATUS_CHOICES = [
        ('Не оплачен', 'Не оплачен'),
        ('Частично оплачен', 'Частично оплачен'),
        ('Оплачен', 'Оплачен'),
        ('Просрочен', 'Просрочен')
    ]
    debtor = models.ForeignKey(Client, verbose_name='Должник', on_delete=models.CASCADE)
    quantity = models.IntegerField("Размер долга")
    amount_meat = models.SmallIntegerField("Количество мяса")
    status = models.CharField('Статус', max_length=40, choices=DEBT_STATUS_CHOICES, default='Не оплачен')
    progress = models.SmallIntegerField("Прогресс оплаты", default=0)
    created = models.DateField("Дата выдачи", default=datetime.today)
    return_date = models.DateField("Дата возврата", blank=True, null=True)
    updated = models.DateField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = 'Долг'
        verbose_name_plural = 'Долги'

    def __str__(self):
        return f"{self.debtor} - {self.quantity}"