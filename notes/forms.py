from django import forms
from .models import Note, Categories


class NoteForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Категорії'
    )

    class Meta:
        model = Note
        fields = ['title', 'text', 'reminder', 'is_done']
        labels = {
            'title': 'Назва',
            'text': 'Текст',
            'reminder': 'Нагадування',
            'is_done': 'Виконано',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'reminder': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['categories'].initial = self.instance.categories.all()


class CategoriesForm(forms.ModelForm):
    notes = forms.ModelMultipleChoiceField(
        queryset=Note.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Нотатки'
    )

    class Meta:
        model = Categories
        fields = ['name_categories', 'notes']
        labels = {
            'name_categories': 'Назва категорії',
        }
        widgets = {
            'name_categories': forms.TextInput(attrs={'class': 'form-control'}),
        }
