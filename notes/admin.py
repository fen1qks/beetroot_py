from django.contrib import admin
from .models import Note, Categories


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'reminder', 'is_done')
    list_filter = ('reminder', 'is_done', 'user')
    search_fields = ('title', 'text', 'user__username')


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name_categories',)
    search_fields = ('name_categories',)
