# Generated by Django 4.2.3 on 2023-07-31 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_aboutus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='delivery_address',
            field=models.CharField(max_length=100, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='form',
            field=models.CharField(max_length=50, verbose_name='Форма торта'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='topping',
            field=models.CharField(max_length=50, verbose_name='Топпинг торта'),
        ),
    ]
