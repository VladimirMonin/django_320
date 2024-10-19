from django import forms
from .models import Comment, Category, Tag, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ваш комментарий...'}),
        }
        labels = {
            'text': 'Текст комментария',
        }

class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название категории'}),
    )
    
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории',
        }
        help_texts = {
            'name': 'Введите название категории (от 3 до 200 символов)',
        }
        min_length = {
            'name': 3,
        }
        max_length = {
            'name': 200,
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("Категория с таким названием уже существует.")
        return name

class TagForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название тега'}),
        label='Название тега'
    )
    
    class Meta:
        model = Tag
        fields = ['name']

    def save(self, commit=True):
        """
        Тут можно переопределить логику сохранения. 
        Как правило это добавление связанных данных или т.п.
        """
        return tag
    
    def clean_name(self):

        # TODO проверить HTML html - одно вызовет ошибку формы, другое упадет уже из базы
        name = self.cleaned_data['name']
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError("Тег с таким названием уже существует.")
        return name


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Категория'
    )

    tags = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите теги через запятую'})
)

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'tags', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите теги через запятую'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Текст поста',
            'tags': 'Теги',
            'cover_image': 'Обложка',
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            return [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        return []

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self._save_tags(instance)
        return instance

    def save_tags(self, instance):
        instance.tags.clear()
        for tag_name in self.cleaned_data.get('tags', []):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)