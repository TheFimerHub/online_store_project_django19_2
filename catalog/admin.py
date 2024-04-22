from django.contrib import admin

from catalog.models import Product, Category, Contact, Version


# admin.site.register(Product)
# admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_per_unit', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product',
                    'version_number',
                    'version_name',
                    'is_active',
                    )
