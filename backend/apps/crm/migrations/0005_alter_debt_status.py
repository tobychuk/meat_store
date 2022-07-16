# Generated by Django 3.2.9 on 2022-07-16 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_debt_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='status',
            field=models.CharField(choices=[('Не оплачен', 'Не оплачен'), ('Частично оплачен', 'Частично оплачен'), ('Оплачен', 'Оплачен'), ('Просрочен', 'Просрочен')], default=('Не оплачен', 'Не оплачен'), max_length=40, verbose_name='Статус'),
        ),
    ]