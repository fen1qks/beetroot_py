from django.urls import path
from .views import show_headers, notes_list, notes, NotesPageView, NoteCreateView, NoteUpdateView, NoteDeleteView, \
    CategoriesCreateView, CategoriesUpdateView, CategoriesDeleteView

urlpatterns = [
    path('show_headers/', show_headers, name='show_headers'),
    path('notes_list/', notes_list, name='notes_list'),
    path('notes/', NotesPageView.as_view(), name='notes_page'),
    path('notes/add/', NoteCreateView.as_view(), name='note_add'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),

    path('categories/add/', CategoriesCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoriesUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoriesDeleteView.as_view(), name='category_delete'),
]