from django.shortcuts import render, HttpResponse, get_object_or_404
from .dataset import dataset
from .models import Post, Tag, Category
from django.db.models import F, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .templatetags.md_to_html import markdown_to_html
from .forms import CommentForm, CategoryForm, TagForm, PostForm
from django.shortcuts import render, redirect
from .models import Post, Tag
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
# Декоратор для ограничения доступа к определенным страницам - @login_required, @permission_required
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"},
]

def blog(request):
    search_query = request.GET.get("search", "")
    search_category = request.GET.get("search_category")
    search_tag = request.GET.get("search_tag")
    search_comments = request.GET.get("search_comments")
    page_number = request.GET.get('page', 1)
    
    posts = Post.objects.prefetch_related('tags', 'comments').select_related('author', 'category').filter(status="published")

    if search_query:
        query = Q(title__icontains=search_query) | Q(text__icontains=search_query) 
        
        if search_category:
            query |= Q(category__name__icontains=search_query)
        
        if search_tag:
            query |= Q(tags__name__icontains=search_query)
        
        if search_comments:
            query |= Q(comment__text__icontains=search_query)
        
        posts = posts.filter(query)

    posts = posts.distinct().order_by("-created_at")

    paginator = Paginator(posts, 4)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    breadcrumbs = [
        {'name': 'Главная', 'url': reverse('main')},
        {'name': 'Блог'},
    ]
    return render(request, 'blog_app/blog.html', {
        'posts': posts,
        'breadcrumbs': breadcrumbs,
        'menu': menu,
        'page_alias': 'blog'
    })



def post_by_slug(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    breadcrumbs = [
        {'name': 'Главная', 'url': reverse('main')},
        {'name': 'Блог', 'url': reverse('blog')},
        {'name': post.title}
    ]

    if f'post_{post.id}_viewed' not in request.session:
        Post.objects.filter(id=post.id).update(views=F('views') + 1)
        request.session[f'post_{post.id}_viewed'] = True

    post.refresh_from_db()  # Обновляем объект post после изменения

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                # Создаем комментарий, но пока не сохраняем в базу
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.status = 'unchecked'  # Устанавливаем статус "Не проверен"
                comment.save()
                messages.success(request, 'Ваш комментарий находится на модерации.')
                return redirect('post_by_slug', post_slug=post_slug)
        else:
            messages.error(request, 'Для добавления комментария необходимо войти в систему.')
            return redirect('login')
    else:
        form = CommentForm()

    # Пагинация комментариев
    comments_list = post.comments.filter(status='accepted').order_by('created_at')
    paginator = Paginator(comments_list, 20)  # 5 комментариев на страницу
    page_number = request.GET.get('page')

    try:
        comments_page = paginator.page(page_number)
    except PageNotAnInteger:
        comments_page = paginator.page(1)
    except EmptyPage:
        comments_page = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'form': form,
        'comments': comments_page,
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'blog_app/post_detail.html', context)


class IdexView(TemplateView):
    # Указываем имя шаблона для отображения страницы
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст от родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст глобальное меню сайта
        context["menu"] = menu
        # Устанавливаем идентификатор текущей страницы
        context["page_alias"] = "main"
        return context

class AboutView(View):
    """
    Класс-представление для отображения страницы "О проекте".
    
    Методы:
        get(request) - обрабатывает GET-запросы к странице
        
    Атрибуты:
        breadcrumbs - список навигационных ссылок (хлебные крошки)
        menu - глобальное меню сайта
        page_alias - идентификатор текущей страницы
        
    Шаблон: about.html
    
    Контекст шаблона:
        - breadcrumbs: список словарей с навигационными ссылками
        - menu: список пунктов главного меню
        - page_alias: строка-идентификатор страницы
    """
    def get(self, request):
        breadcrumbs = [
        {'name': 'Главная', 'url': reverse('main')},
        {'name': 'О проекте'},
    ]
        return render(request, 'about.html', {
            'breadcrumbs': breadcrumbs,
            'menu': menu,
            'page_alias': 'about'

        })    

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=True, author=request.user)
            messages.success(request, 'Пост успешно создан и отправлен на модерацию.')
            return redirect('add_post')
    else:
        form = PostForm()

    return render(request, 'blog_app/add_post.html', {'form': form, 'menu': menu})


@login_required
def update_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно обновлен и отправлен на модерацию.')
            return redirect('update_post', post_slug=post_slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog_app/add_post.html', {'form': form, 'menu': menu})


class PostsByTagListView(ListView):
    """
    Класс-представление для отображения списка постов по тегу.
    """
    model = Post
    template_name = 'blog_app/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        posts = Post.objects.filter(tags__slug=tag).filter(status='published')
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'blog'
        return context




def posts_by_category(request, category):
    """
    Функция представления для отображения страницы постов с определенной категорией.
    """
    context = {
        # Можно получить все посты со стороны тега, используя related_name posts в модели Tag
        # Tag.objects.get(slug=tag).posts.all()
        "posts": Category.objects.get(slug=category).posts.all(),
        "menu": menu,
        "page_alias": "blog",
    }
    return render(request, "blog_app/blog.html", context=context)


# @csrf_exempt # Отключает проверку CSRF токена при пост запросах для этой вью
def preview_post(request):
    """
    Вью которая работает на AJAX запросы, и дает предпросмотр постов при создании нового поста.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        html = markdown_to_html(text)
        return JsonResponse({"html": html})


class AddCategoryView(LoginRequiredMixin, View):
    """
    Класс-представление для добавления новой категории.
    
    Методы:
        get(request) - обрабатывает GET-запросы, отображает форму для создания категории
        post(request) - обрабатывает POST-запросы, сохраняет новую категорию
        
    Атрибуты контекста:
        menu - глобальное меню сайта
        form - форма для создания категории (CategoryForm)
        operation_title - заголовок операции
        operation_header - заголовок формы
        submit_button_text - текст кнопки отправки формы
        
    Шаблон: category_form.html
    
    Сообщения:
        - Успех: "Категория '{name}' успешно добавлена!"
        - Ошибка: "Пожалуйста, исправьте ошибки ниже."
        
    Редиректы:
        - После успешного создания: add_category
        - При ошибке валидации: add_category
    """
    def get(self, request):
        # Формируем контекст для отображения формы добавления категории
        context = {
            "menu": menu,
            "form": CategoryForm(),
            "operation_title": "Добавить категорию",
            "operation_header": "Добавить новую категорию",
            "submit_button_text": "Создать",
        }
        # Отображаем шаблон с формой для создания категории
        return render(request, "blog_app/category_form.html", context)
    
    def post(self, request):
        # Создаем форму на основе полученных POST данных
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Сохраняем новую категорию в базу данных
            form.save()
            # Добавляем сообщение об успешном создании категории
            messages.success(request, f"Категория '{form.cleaned_data['name']}' успешно добавлена!")
            return redirect('add_category')
        else:
            # В случае ошибки валидации формы, добавляем сообщение об ошибке
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")
            return redirect('add_category')        


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    """
    Класс-представление для обновления категории.
    Наследуется от UpdateView для редактирования объектов и LoginRequiredMixin для ограничения доступа
    только авторизованным пользователям
    """
    model = Category
    form_class = CategoryForm
    template_name = "blog_app/category_form.html"
    
        
    def get_object(self, queryset=None):
        """Метод для получения объекта категории по slug из URL"""
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])
    
    def get_success_url(self):
        """Метод определяет URL для перенаправления после успешного обновления категории"""
        # category/<slug:category>/
        return reverse_lazy('posts_by_category', kwargs={'category': self.object.slug})
    
    def get_context_data(self, **kwargs):
        """Метод для передачи дополнительных данных в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["operation_title"] = "Обновить категорию"
        context["operation_header"] = "Обновить категорию"
        context["submit_button_text"] = "Сохранить"
        return context
    
    def form_valid(self, form):
        """Метод вызывается при успешной валидации формы"""
        response = super().form_valid(form)
        messages.success(self.request, f"Категория '{form.cleaned_data['name']}' успешно обновлена.")
        return response
    
    def form_invalid(self, form):
        """Метод вызывается при неуспешной валидации формы"""
        messages.error(self.request, "Пожалуйста, исправьте ошибки ниже.")
        return super().form_invalid(form)

class AddTagView(LoginRequiredMixin, CreateView):
    """
    Класс-представление для добавления тега.
    Наследуется от CreateView для создания объектов и LoginRequiredMixin для ограничения доступа
    только авторизованным пользователям
    """
    # Указываем модель, с которой будет работать представление
    model = Tag
    # Указываем форму, которую мы описали в froms.py
    form_class = TagForm
    # Указываем путь к шаблону, который будет использоваться для отображения формы
    template_name = "blog_app/add_tag.html"
    success_url = reverse_lazy("add_tag")
    
    # Передаем контекст через расширение метода get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        return context
    
    def form_valid(self, form):
            """Метод вызывается при успешной валидации формы"""
            # Сохраняем форму
            response = super().form_valid(form)
            # Добавляем сообщение об успехе
            messages.success(self.request, f"Тег {form.instance.name} успешно добавлен!")
            return response
    
    def form_invalid(self, form):
        """Метод вызывается при неуспешной валидации формы"""
        # Добавляем сообщение об ошибке
        messages.error(self.request, "Ошибка при добавлении тега. Проверьте введенные данные.")
        return super().form_invalid(form)
    