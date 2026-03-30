
from django.db import models
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    reminder = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('notes')

    def __str__(self):
        return self.title

class Categories(models.Model):
    name_categories = models.CharField(max_length=200)
    notes = models.ManyToManyField(Note, related_name='categories')

    def __str__(self):
        return self.name_categories
