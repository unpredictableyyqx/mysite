# Generated by Django 3.1.2 on 2020-10-13 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gasstation', '0002_auto_20201013_1558'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OderProduct',
            new_name='OrderProduct',
        ),
        migrations.AlterModelTable(
            name='orderproduct',
            table='order_review',
        ),
    ]
