# Generated by Django 3.1.4 on 2021-03-29 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='order',
            new_name='order_id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='product',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='vendor',
            new_name='vendor_id',
        ),
    ]
