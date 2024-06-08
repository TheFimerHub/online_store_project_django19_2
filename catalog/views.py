from django.shortcuts import render, get_object_or_404  # type: ignore
from django.core.files.storage import default_storage  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from catalog.forms import ProductForm, ProductModeratorForm, VersionForm, VersionModeratorForm
from catalog.models import Product, Contact, Version
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from os.path import join
from os.path import basename
from django.core.exceptions import PermissionDenied


class HomePageView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 12
    ordering = ['id']

    def get_queryset(self):
        # Фильтруем продукты: либо есть активная версия, либо нет версии
        return Product.objects.filter(
            Q(versions__is_active=True) | Q(versions__isnull=True)
        ).order_by('last_modified_date').distinct()

    def get_context_data(self, **kwargs):
        # Добавление активных версий продуктов в контекст
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()  # Получаем список продуктов
        active_versions = {}  # Словарь для хранения активных версий

        # Проходимся по каждому продукту и его связанным версиям
        for product in products:
            active_versions[product.id] = []  # Создаем список для каждого продукта
            versions = product.versions.filter(is_active=True)  # Фильтруем активные версии

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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = "/users/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        active_version = product.versions.filter(is_active=True).first()
        context['active_version'] = active_version
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    login_url = "/users/"
    success_url = reverse_lazy('catalog:home_page')

    def form_valid(self, form):
        form.instance.user_owner = self.request.user
        image_preview = form.cleaned_data['image_preview']
        if image_preview:
            file_name = basename(image_preview.name)
            save_path = join('products', file_name)
            default_storage.save(save_path, image_preview)
            form.instance.image_preview = file_name
            print(save_path, form.instance.image_preview)

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/create_product.html'
    login_url = "/users/"
    success_url = reverse_lazy('catalog:home_page')


    def form_valid(self, form):
        # Получаем предыдущий объект продукта (если это обновление)
        previous_product = self.get_object()

        # Проверяем, существует ли поле 'image_preview' в форме
        if 'image_preview' in form.cleaned_data:
            # Получаем новое изображение из формы
            new_image_preview = form.cleaned_data['image_preview']

            # Проверяем, было ли изображение изменено
            if previous_product and previous_product.image_preview != new_image_preview:
                # Сохраняем новое изображение в подпапке products
                file_name = new_image_preview.name
                save_path = 'products/' + file_name
                default_storage.save(save_path, new_image_preview)
                form.instance.image_preview = file_name

                # Удаляем предыдущее изображение, если оно было изменено
                if previous_product.image_preview:
                    if default_storage.exists(previous_product.image_preview.path):
                        default_storage.delete(previous_product.image_preview.path)

        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user

        if user == self.object.user_owner:
            return ProductForm

        if user.has_perm("catalog.can_change_description") and user.has_perm("catalog.can_change_category"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    login_url = "/users/"
    success_url = reverse_lazy('catalog:home_page')

class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'catalog/create_version.html'
    login_url = "/users/"
    success_url = reverse_lazy('catalog:home_page')

    def get_object(self, queryset=None):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(Version, uuid=uuid)

    def get_form_class(self):
        user = self.request.user
        version = self.get_object()

        if user == version.product.user_owner:
            return VersionForm

        if user.has_perm("catalog.can_cancel_publication"):
            return VersionModeratorForm
        raise PermissionDenied
