# Generated by Django 5.1.2 on 2025-01-04 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WareHouse', '0005_inventoryitem_accommodations_alter_inventory_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'verbose_name': 'Выкладка', 'verbose_name_plural': 'Выкладки'},
        ),
        migrations.AlterModelOptions(
            name='inventoryitem',
            options={'verbose_name': 'Товар выкладки', 'verbose_name_plural': 'Товары выкладки'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='shelf',
            options={'verbose_name': 'Полка', 'verbose_name_plural': 'Полки'},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'verbose_name': 'Склад', 'verbose_name_plural': 'Склада'},
        ),
    ]
