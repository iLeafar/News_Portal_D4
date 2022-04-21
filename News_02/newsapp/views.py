from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm



class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    #queryset = Product.objects.filter(price_lt=100)
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10


# class PostDetail(DetailView):
#     # Модель всё та же, но мы хотим получать информацию по отдельному товару
#     model = Post
#     # Используем другой шаблон — product.html
#     template_name = 'post.html'
#     # Название объекта, в котором будет выбранный пользователем продукт
#     context_object_name = 'post'

    # def index(request):
    #     return render(request, 'posts.html')


def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'flatpages/post.html', {'post': post})


class PostSearch(PostsList):
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filter_class = PostFilter

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(CreateView):
    template_name = 'flatpages/add.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

    # def form_valid(self, form):
    #     self.object = services.create_news(form, self.request)
    #
    #     return super(generic.CreateView, self).form_valid(form)


class PostUpdate(UpdateView):
    template_name = 'flatpages/edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'