import pytest

from ..forms import RegisterForm, LoginForm, CategoriesForm, NoteForm
from ..models import Note, Categories


@pytest.mark.django_db
def test_note_form_create(user):
    category = Categories.objects.create(name_categories='Особисте')

    form = NoteForm(data={
        'title': 'Нова нотатка',
        'text': 'Новий текст',
        'reminder': 'on',
        'categories': [category.id],
    })

    assert form.is_valid(), form.errors

    note = form.save(commit=False)
    note.user = user
    note.save()
    note.categories.set(form.cleaned_data['categories'])

    assert note.title == 'Нова нотатка'


@pytest.mark.django_db
def test_note_form_update(note):
    category = Categories.objects.create(name_categories='Оновлена категорія')

    form = NoteForm(
        data={
            'title': 'Нова назва',
            'text': 'Оновлений текст',
            'reminder': 'on',
            'is_done': 'on',
            'categories': [category.id],
        },
        instance=note,
    )

    assert form.is_valid(), form.errors

    updated_note = form.save()
    updated_note.categories.set(form.cleaned_data['categories'])
    updated_note.refresh_from_db()

    assert updated_note.title == 'Нова назва'
    assert updated_note.text == 'Оновлений текст'
    assert updated_note.reminder is True
    assert updated_note.is_done is True
    assert list(updated_note.categories.all()) == [category]


@pytest.mark.django_db
def test_note_form_title_invalid():
    form = NoteForm(data={
        'title': '',
        'text': 'Текст нотатки',
        'reminder': False,
        'is_done': False,
    })

    assert not form.is_valid()
    assert 'title' in form.errors


@pytest.mark.django_db
def test_note_form_text_invalid():
    form = NoteForm(data={
        'title': 'Нотатка',
        'text': '',
        'reminder': False,
        'is_done': False,
    })

    assert not form.is_valid()
    assert 'text' in form.errors


@pytest.mark.django_db
def test_note_form_sets_categories(note, category):
    note.categories.add(category)

    form = NoteForm(instance=note)

    assert list(form.fields['categories'].initial) == [category]

@pytest.mark.django_db
def test_categories_form_create(user):
    my_note = Note.objects.create(user=user, title='Моя нотатка', text='Текст')

    form = CategoriesForm(
        data={
            'name_categories': 'Нова категорія',
            'notes': [my_note.pk],
        },
        user=user,
    )

    assert form.is_valid(), form.errors

    category = form.save()
    category.refresh_from_db()

    assert category.name_categories == 'Нова категорія'
    assert list(category.notes.all()) == [my_note]


@pytest.mark.django_db
def test_categories_form_update(user, category):
    my_note = Note.objects.create(user=user, title='Нотатка для update', text='Текст')

    form = CategoriesForm(
        data={
            'name_categories': 'Оновлена категорія',
            'notes': [my_note.pk],
        },
        instance=category,
        user=user,
    )

    assert form.is_valid(), form.errors

    updated_category = form.save()
    updated_category.refresh_from_db()

    assert updated_category.name_categories == 'Оновлена категорія'
    assert list(updated_category.notes.all()) == [my_note]


def test_login_form_valid():
    form = LoginForm(data={
        'username': 'testuser',
        'password': 'SuperPass123',
    })

    assert form.is_valid()


@pytest.mark.django_db
def test_register_form_valid():
    form = RegisterForm(data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'SuperPass123',
        'password2': 'SuperPass123',
    })

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_register_form_password_invalid():
    form = RegisterForm(data={
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password1': 'SuperPass123',
        'password2': 'WrongPass123',
    })

    assert not form.is_valid()
    assert 'password2' in form.errors or '__all__' in form.errors