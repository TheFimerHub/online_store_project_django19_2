from django.shortcuts import render  # type: ignore
from django.core.files.storage import default_storage  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from catalog.models import Product, Contact


def home_page(request):
    products = Product.objects.order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': page_obj
    }

    return render(request, 'catalog/home.html', context)


def contacts_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
        Contact.objects.create(name=name, phone=phone, message=message)

    return render(request, 'catalog/contacts.html')


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)


# доп. задание
def create_product(request):
    context = {'product_created': False}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')
        category = request.POST.get('category')
        price_per_unit = request.POST.get('price')

        if image_file:
            file_name = image_file.name
            default_storage.save('products/' + file_name, image_file)
            image_preview = file_name
        else:
            image_preview = None

        try:
            Product.objects.create(name=name, description=description, image_preview=image_preview, category=category,
                                   price_per_unit=price_per_unit)
            context = {'product_created': True}
        except Exception:
            context = {'product_created': False}
    return render(request, 'catalog/create_product.html', context)
