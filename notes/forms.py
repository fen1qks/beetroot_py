from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        queryset=Note.objects.none(),
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['notes'].queryset = Note.objects.filter(user=user).order_by('title')
        else:
            self.fields['notes'].queryset = Note.objects.none()


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=65,
        label="Ім'я користувача",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=65,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
