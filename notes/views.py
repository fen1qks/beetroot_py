from django.http import HttpResponse

from django.shortcuts import render

from notes.models import Categories

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Note
from .forms import NoteForm, CategoriesForm


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
            'time': "10.03.2026",
            'description': 'Description 1'
        },
        {
            'name': 'Name 2',
            'time': '11.03.2026',
            'description': 'Description 2'
        }
    ]
    return render(request, 'index.html', {'notes': notes})

def notes(request):
    categories = Categories.objects.prefetch_related('notes').all()
    return render(request, 'notes.html', {'categories': categories})

class NotesPageView(ListView):
    model = Categories
    template_name = 'notes.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Categories.objects.prefetch_related('notes').all()

class CategoriesUpdateView(UpdateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('notes_page')

class CategoriesCreateView(CreateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('notes_page')

class CategoriesUpdateView(UpdateView):
    model = Categories
    form_class = CategoriesForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('notes_page')

class CategoriesDeleteView(DeleteView):
    model = Categories
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('notes_page')

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('notes_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        categories = form.cleaned_data['categories']
        self.object.categories.set(categories)
        return response

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('notes_page')

    def form_valid(self, form):
        response = super().form_valid(form)
        categories = form.cleaned_data['categories']
        self.object.categories.set(categories)
        return response

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('notes_page')
