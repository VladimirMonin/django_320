from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import User
from python_blog import settings


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно. Вы можете войти.')
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Вы успешно вошли как {username}.')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('main')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('main')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем, является ли текущий пользователь владельцем профиля
        context['is_owner'] = self.request.user == self.object
        
        if context['is_owner']:
            # Проверяем подписку на бота
            context['is_subscribed'] = bool(self.object.tg_chat_id)
            # Формируем ссылку на бота
            # https://t.me/nova_test88_bot?start=f73756ca-83fd-40da-9247-5dfd4548e9ed
            context['bot_link'] = f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={self.object.uuid}"
            
        return context
