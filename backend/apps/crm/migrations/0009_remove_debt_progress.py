# Generated by Django 3.2.9 on 2022-07-20 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20220719_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debt',
            name='progress',
        ),
    ]