from django.urls import path
from .views import show_headers, notes_list, notes_from_db

urlpatterns = [
    path('show_headers/', show_headers, name='show_headers'),
    path('notes_list/', notes_list, name='notes_list'),
    path('notes/', notes_from_db, name='notes_from_db')
]