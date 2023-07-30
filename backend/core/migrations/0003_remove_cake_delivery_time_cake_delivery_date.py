# Generated by Django 4.2.3 on 2023-07-30 20:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_cake_delivery_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cake',
            name='delivery_time',
        ),
        migrations.AddField(
            model_name='cake',
            name='delivery_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Время доставки'),
        ),
    ]
