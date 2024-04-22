from django.shortcuts import render, get_object_or_404  # type: ignore
from django.core.files.storage import default_storage  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from catalog.forms import ProductForm
from catalog.models import Product, Contact, Version
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from .models import Product, Version
from django.db.models import Q


class HomePageView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['id']

    def get_queryset(self):
        # Фильтруем продукты: либо есть активная версия, либо нет версии
        return Product.objects.filter(Q(version__is_active=True) | Q(version__isnull=True)).order_by('last_modified_date').distinct()

    def get_context_data(self, **kwargs):
        # Добавление активных версий продуктов в контекст
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()  # Получаем список продуктов
        active_versions = {}  # Словарь для хранения активных версий

        # Проходимся по каждому продукту и его связанным версиям
        for product in products:
            active_versions[product.id] = []  # Создаем список для каждого продукта
            versions = product.version_set.filter(is_active=True)  # Фильтруем активные версии

            for version in versions:
                active_versions[product.id].append({
                    'version_name': version.version_name,
                    'version_number': version.version_number,
                })

        context['active_versions'] = active_versions  # Добавляем активные версии в контекст

        # Получаем страницу из GET-параметров запроса
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        # Определение диапазона страниц для пагинации
        page_numbers_range = 5  # кол-во страниц, отображаемых в "page navigation"
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        paginator = context['paginator']
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:home_page')

    def form_valid(self, form):
        image_preview = form.cleaned_data['image_preview']
        if image_preview:
            file_name = image_preview.name
            default_storage.save('products/' + file_name, image_preview)
            form.instance.image_preview = file_name

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    success_url = reverse_lazy('catalog:home_page')

    def form_valid(self, form):
        # Получаем предыдущий объект продукта
        previous_product = self.get_object()

        # Удаляем предыдущее изображение, если оно было изменено
        new_image_preview = form.cleaned_data['image_preview']
        if new_image_preview:
            if previous_product.image_preview:
                default_storage.delete(previous_product.image_preview.path)

            # Сохраняем новое изображение
            file_name = new_image_preview.name
            default_storage.save('products/' + file_name, new_image_preview)
            form.instance.image_preview = 'products/' + file_name

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:home_page')
