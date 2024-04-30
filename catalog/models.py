from django.db import models

from users.models import User

NULLABLE = {'null' : True, 'blank' : True}

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    description = models.TextField(max_length=500, verbose_name='description')
    image_preview = models.ImageField(verbose_name='image', **NULLABLE)
    category = models.CharField(max_length=50, verbose_name='сategory')
    price_per_unit = models.PositiveIntegerField(verbose_name='price')
    creation_date = models.DateField(auto_now_add=True, verbose_name='creation date')
    last_modified_date = models.DateField(auto_now=True, verbose_name='last modified date')
    user_owner = models.ForeignKey(User, verbose_name='user owner', **NULLABLE, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_image_url(self):
        print(self.image_preview)
        if self.image_preview:
            return f"products/{self.image_preview}"
        return ''

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_number = models.FloatField(default=1)
    version_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    description = models.TextField(max_length=250, verbose_name='description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, **NULLABLE)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


