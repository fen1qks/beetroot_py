from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    reminder = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

class Categories(models.Model):
    name_categories = models.CharField(max_length=200)
    notes = models.ManyToManyField(Note, related_name='note')
