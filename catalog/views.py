from django.shortcuts import render  # type: ignore

from catalog.models import Product, Contact


def home_page(request):
    # доп. задание
    latest_products = Product.objects.order_by('-creation_date')[:5]

    print("Последние 5 товаров:")
    for product in latest_products:
        print(product.name)

    return render(request, 'catalog/home.html')

def contacts_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
        # доп. задание
        Contact.objects.create(name=name, phone=phone, message=message)

    return render(request, 'catalog/contacts.html')