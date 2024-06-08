# Generated by Django 4.2 on 2024-05-31 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_product_user_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_cancel_publication', 'Can cancel product publication'), ('can_change_description', 'Can change product description'), ('can_change_category', 'Can change product category')], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]