import pytest

from ..models import Note, Categories


@pytest.mark.django_db
def test_note_creation(user):
    note = Note.objects.create(
        user=user,
        title='Назва нотатки',
        text='Опис нотатки',
        reminder=True,
        is_done=False,
    )

    assert note.user == user
    assert note.title == 'Назва нотатки'

@pytest.mark.django_db
def test_note_str(note):
    assert str(note) == note.title

@pytest.mark.django_db
def test_category_creation():
    category = Categories.objects.create(name_categories='Робота')
    assert category.id is not None
    assert str(category) == 'Робота'

@pytest.mark.django_db
def test_user_delete_cascades_notes(user):
    note = Note.objects.create(
        user=user,
        title='Тимчасова нотатка',
        text='Буде видалена разом з юзером',
    )
    note_id = note.id

    user.delete()

    assert not Note.objects.filter(id=note_id).exists()

@pytest.mark.django_db
def test_note_create(user):
    note = Note.objects.create(
        user=user,
        title='Нотатка створена',
        text='Текст',
        reminder=True,
        is_done=False,
    )

    assert Note.objects.filter(pk=note.pk).exists()
    assert note.user == user
    assert note.title == 'Нотатка створена'


@pytest.mark.django_db
def test_note_update(note):
    note.title = 'Оновлена назва'
    note.text = 'Оновлений текст'
    note.reminder = True
    note.is_done = True
    note.save()

    note.refresh_from_db()
    assert note.title == 'Оновлена назва'
    assert note.text == 'Оновлений текст'
    assert note.reminder is True
    assert note.is_done is True

@pytest.mark.django_db
def test_note_delete(note):
    note_id = note.pk

    note.delete()

    assert not Note.objects.filter(pk=note_id).exists()

@pytest.mark.django_db
def test_categories_create():
    category = Categories.objects.create(name_categories='Нова категорія')

    assert Categories.objects.filter(pk=category.pk).exists()
    assert str(category) == 'Нова категорія'

@pytest.mark.django_db
def test_categories_update(category):
    category.name_categories = 'Оновлена категорія'
    category.save()

    category.refresh_from_db()
    assert category.name_categories == 'Оновлена категорія'

@pytest.mark.django_db
def test_categories_delete(category):
    category_id = category.pk

    category.delete()

    assert not Categories.objects.filter(pk=category_id).exists()

@pytest.mark.django_db
def test_categories_update_notes_relation(note):
    category = Categories.objects.create(name_categories='Зв’язки')
    second_note = Note.objects.create(
        user=note.user,
        title='Друга нотатка',
        text='Текст другої нотатки',
    )

    category.notes.add(note)
    category.notes.add(second_note)

    assert category.notes.count() == 2
    assert set(category.notes.values_list('pk', flat=True)) == {note.pk, second_note.pk}

@pytest.mark.django_db
def test_categories_remove_note_relation(note):
    category = Categories.objects.create(name_categories='Прибрати зв’язок')
    category.notes.add(note)

    category.notes.remove(note)

    assert note not in category.notes.all()

@pytest.mark.django_db
def test_note_can_exist_without_user():
    note = Note.objects.create(
        title='Без автора',
        text='Але модель це дозволяє',
    )
    assert note.user is None
