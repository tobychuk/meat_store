from django.db import models

# Create your models here.

class Client(models.Model):
    first_name = models.CharField('Имя', max_length=15)
    last_name = models.CharField("Фамилия", max_length=15)
    middle_name = models.CharField("Отчество", max_length=15)
    phone_number = models.IntegerField("Телефонный номер")
    reserve_phone_number = models.IntegerField("Запасной телефонный номер", blank=True)
    address = models.CharField("Адрес проживания")
    passport_image_first = models.ImageField("Фото лицевой стороны паспорта")
    passport_image_second = models.ImageField("Фото задней стороны паспорта")

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Debt(models.Model):
    debtor = models.ForeignKey(Client, verbose_name='Должник', on_delete=models.CASCADE)
    quantity = models.IntegerField("Размер долга")
    amount_meat = models.SmallIntegerField("Количество мяса")
    created = models.DateTimeField("Дата создания")
    updated = models.DateTimeField("Обновлено")