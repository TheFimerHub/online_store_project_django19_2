# Generated by Django 5.0.2 on 2024-02-13 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=250, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=50, verbose_name='сategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=250, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_preview',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified_date',
            field=models.DateField(auto_now=True, verbose_name='last modified date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_per_unit',
            field=models.PositiveIntegerField(verbose_name='price'),
        ),
    ]
