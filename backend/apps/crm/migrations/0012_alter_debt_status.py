# Generated by Django 3.2.9 on 2022-07-22 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_auto_20220722_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='status',
            field=models.CharField(choices=[('Not paid', 'Не оплачен'), ('Paid', 'Оплачен')], default='Not Paid', max_length=40, verbose_name='Статус'),
        ),
    ]
