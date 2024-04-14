from django.shortcuts import render  # type: ignore
from django.core.files.storage import default_storage  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from catalog.models import Product, Contact
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy


class HomePageView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # кол-во страниц, отображаемых в "page navigation"
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= paginator.num_pages:
            end_index = paginator.num_pages

        page_range = list(paginator.page_range)[start_index:end_index]

        context['page_range'] = page_range
        return context


class ContactsPageView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
        Contact.objects.create(name=name, phone=phone, message=message)
        return self.render_to_response(self.get_context_data())


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

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
