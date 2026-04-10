from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .forms import NoteForm, CategoriesForm, RegisterForm, LoginForm
from .models import Note, Categories


def show_headers(request):
    headers = request.META
    html = "<h1>HTTP-заголовки запиту</h1><table border='1'>"
    html += "<tr><th>Заголовок</th><th>Значення</th></tr>"

    for key, value in headers.items():
        if key.startswith("HTTP_"):
            header_name = key[5:].replace('_', '-').title()
            html += f"<tr><td>{header_name}</td><td>{value}</td></tr>"
    html += "</table>"
    return HttpResponse(html)


def notes_list(request):
    notes = [
        {
            'name': 'Name 1',
            'time': '10.03.2026',
            'description': 'Description 1'
        },
        {
            'name': 'Name 2',
            'time': '11.03.2026',
            'description': 'Description 2'
        }
    ]
    return render(request, 'index.html', {'notes': notes})


class NotesPageView(LoginRequiredMixin, ListView):
    model = Categories
    template_name = 'notes.html'
    context_object_name = 'categories'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user_notes = Note.objects.filter(user=self.request.user).order_by('title')
        return Categories.objects.prefetch_related(
            Prefetch('notes', queryset=user_notes)
        ).order_by('name_categories')


class CategoriesCreateView(LoginRequiredMixin, CreateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('notes_page')
    login_url = reverse_lazy('login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CategoriesUpdateView(LoginRequiredMixin, UpdateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('notes_page')
    login_url = reverse_lazy('login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CategoriesDeleteView(LoginRequiredMixin, DeleteView):
    model = Categories
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('notes_page')
    login_url = reverse_lazy('login')


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('notes_page')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('notes_page')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.categories.set(form.cleaned_data['categories'])
        return response


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('notes_page')
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('notes_page')

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Вітаємо, {username}')
            return redirect('notes_page')

        messages.error(request, 'Невірний логін або пароль')

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('notes_page')

    if request.method == "GET":
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Реєстрація успішна')
        return redirect('notes_page')

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect('login')
