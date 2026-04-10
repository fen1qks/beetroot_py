from django.conf import settings
from django.db import models
from django.urls import reverse


class Note(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True,
        verbose_name='Користувач',
    )
    title = models.CharField(max_length=100, verbose_name='Назва')
    text = models.CharField(max_length=100, verbose_name='Текст')
    reminder = models.BooleanField(default=False, verbose_name='Нагадування')
    is_done = models.BooleanField(default=False, verbose_name='Виконано')

    def get_absolute_url(self):
        return reverse('notes_page')

    def __str__(self):
        return self.title


class Categories(models.Model):
    name_categories = models.CharField(max_length=200, verbose_name='Назва категорії')
    notes = models.ManyToManyField(Note, related_name='categories', blank=True, verbose_name='Нотатки')

    def __str__(self):
        return self.name_categories
