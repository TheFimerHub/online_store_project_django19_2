from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from posts.models import Post
from django.core.files.storage import default_storage  # type: ignore
from pytils.translit import slugify


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'preview']

    def form_valid(self, form):
        # Обработка slug
        new_post = form.save(commit=False)
        new_post.slug = self.get_unique_slug(new_post.title)
        new_post.save()

        # Обработка изображения
        preview = form.cleaned_data['preview']
        if preview:
            file_name = preview.name
            default_storage.save('posts/' + file_name, preview)
            form.instance.preview = file_name

        return super().form_valid(form)

    def get_unique_slug(self, title):
        # Сохранение slug
        slug = slugify(title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def get_success_url(self):
        return reverse('posts:view', kwargs={'slug': self.object.slug})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 4
    ordering = ['-creation_date', '-id']

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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset =  queryset.filter(publication_sign=True)
        return queryset

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class PostUpdateView(UpdateView):
    model = Post
    context_object_name = 'post'
    fields = ['title', 'content', 'preview']

    def form_valid(self, form):
        preview = form.cleaned_data.get('preview')
        if preview:
            file_name = preview.name
            default_storage.save('posts/' + file_name, preview)
            form.instance.preview = file_name
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:view', kwargs={'slug': self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = reverse_lazy('posts:index')
