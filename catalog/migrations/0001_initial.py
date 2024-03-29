# Generated by Django 5.0.2 on 2024-02-13 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Category name')),
                ('description', models.TextField(max_length=250, verbose_name='Category description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Product name')),
                ('description', models.TextField(max_length=250, verbose_name='Product description')),
                ('image_preview', models.ImageField(upload_to='product_images/', verbose_name='Product image')),
                ('category', models.CharField(max_length=50, verbose_name='Product category')),
                ('price_per_unit', models.PositiveIntegerField(verbose_name='Product price')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Product creation date')),
                ('last_modified_date', models.DateField(auto_now=True, verbose_name='Product last modified date')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
