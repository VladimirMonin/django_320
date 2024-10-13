from django import forms
from .models import Comment

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

# форма не связанная с моделью
class CategoryForm(forms.Form):
    name = forms.CharField(max_length=200, min_length=3, 
                           label='Название категории', required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название категории'}))