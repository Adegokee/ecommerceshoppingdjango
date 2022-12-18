# Generated by Django 4.0.4 on 2022-12-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_phone_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line_1',
            field=models.TextField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='order',
            name='address_line_2',
            field=models.TextField(blank=True, max_length=70),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
