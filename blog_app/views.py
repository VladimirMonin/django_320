from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from .forms import CommentForm, CategoryForm, TagForm, PostForm
from .models import Post, Tag, Category, Comment
from .templatetags.md_to_html import markdown_to_html
import json
from django.utils.decorators import method_decorator


menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"},
]

class BlogView(ListView):
    model = Post
    template_name = 'blog_app/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        # Базовый QuerySet с предзагрузкой связанных данных
        queryset = Post.objects.prefetch_related('tags', 'comments').select_related('author', 'category').filter(status="published")
        
        # Получаем параметры поиска из GET-запроса
        search_query = self.request.GET.get("search", "")
        search_category = self.request.GET.get("search_category")
        search_tag = self.request.GET.get("search_tag")
        search_comments = self.request.GET.get("search_comments")

        if search_query:
            query = Q(title__icontains=search_query) | Q(text__icontains=search_query)
            
            if search_category:
                query |= Q(category__name__icontains=search_query)
            
            if search_tag:
                query |= Q(tags__name__icontains=search_query)
            
            if search_comments:
                query |= Q(comments__text__icontains=search_query)
            
            queryset = queryset.filter(query)

        return queryset.distinct().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'blog'
        context['breadcrumbs'] = [
            {'name': 'Главная', 'url': reverse('main')},
            {'name': 'Блог'},
        ]
        return context


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_by_slug', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем только родительские комментарии
        comments_list = self.object.comments.filter(
            status='accepted',
            parent=None
        ).order_by('created_at')
        
        paginator = Paginator(comments_list, 20)
        page_number = self.request.GET.get('page')

        try:
            comments_page = paginator.page(page_number)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = paginator.page(paginator.num_pages)

        context['comments'] = comments_page
        context['form'] = self.get_form()
        context['menu'] = menu
        context['breadcrumbs'] = [
            {'name': 'Главная', 'url': reverse('main')},
            {'name': 'Блог', 'url': reverse('blog')},
            {'name': self.object.title}
        ]
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Для добавления комментария необходимо войти в систему.')
            return redirect('login')

        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.status = 'unchecked'
            
            # Обработка родительского комментария
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                # Проверяем, что родительский комментарий не является ответом
                if parent_comment.is_parent():
                    comment.parent = parent_comment
            
            comment.save()
            messages.success(request, 'Ваш комментарий находится на модерации.')
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)



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

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/add_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=True, author=self.request.user)
        return JsonResponse({
            'success': True,
            'message': 'Пост успешно создан',
            'redirect_url': reverse('blog')
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Ошибка в форме',
            'errors': form.errors
        }, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/add_post.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs['post_slug'])

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            'success': True,
            'message': 'Пост успешно обновлен',
            'redirect_url': reverse('post_by_slug', kwargs={'slug': self.object.slug})
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Ошибка в форме',
            'errors': form.errors
        }, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


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


class PostsByCategoryListView(ListView):
    model = Post
    template_name = 'blog_app/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.select_related('author', 'category')\
                         .prefetch_related('tags', 'comments')\
                         .filter(category__slug=category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'blog'
        context['breadcrumbs'] = [
            {'name': 'Главная', 'url': reverse('main')},
            {'name': 'Блог', 'url': reverse('blog')},
            {'name': Category.objects.get(slug=self.kwargs['category']).name}
        ]
        return context




class PreviewPostView(View):
    """
    Класс-представление для предпросмотра постов через AJAX
    """
    http_method_names = ['post']  # Явно указываем разрешенный метод
    
    def post(self, request, *args, **kwargs):
        # Получаем данные из тела AJAX-запроса в формате JSON
        data = json.loads(request.body)
        # Извлекаем текст поста из данных с пустой строкой как значение по умолчанию
        text = data.get("text", "")
        # Преобразуем markdown-разметку в HTML для предпросмотра
        html = markdown_to_html(text)
        # Отправляем готовый HTML в формате JSON обратно клиенту
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




class LikePostView(LoginRequiredMixin, View):

    # Маршрут для авторизации псевдоним login
    # login_url = 'users/login/'
    # login_url = reverse_lazy('login')
    #TODO Сделать работающим перенаправление!
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        user = request.user

        if post.likes.filter(id=user.id).exists():
            # Пользователь уже лайкнул пост, удаляем лайк
            post.likes.remove(user)
            liked = False
        else:
            # Пользователь еще не лайкнул пост, добавляем лайк
            post.likes.add(user)
            liked = True

        # Возвращаем обновленные данные о лайках
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
