# Generated by Django 3.2.9 on 2022-07-16 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_alter_debt_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='status',
            field=models.CharField(choices=[('None', 'Клиент не выбран'), ('Не оплачен', 'Не оплачен'), ('Частично оплачен', 'Частично оплачен'), ('Оплачен', 'Оплачен'), ('Просрочен', 'Просрочен')], default='Не оплачен', max_length=40, verbose_name='Статус'),
        ),
    ]
