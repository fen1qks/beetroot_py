from django import forms
from .models import Note, Categories

class NoteForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Note
        fields = ['title', 'text', 'reminder','is_done']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()

class CategoriesForm(forms.ModelForm):
    notes = forms.ModelMultipleChoiceField(
        queryset=Note.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Categories
        fields = ['name_categories', 'notes']
