import pytest

from .factories import CategoriesFactory, NoteFactory, UserFactory


@pytest.fixture
def user(db):
    return UserFactory(username='testuser', password='testpass123')


@pytest.fixture
def another_user(db):
    return UserFactory(username='anotheruser', password='testpass123')


@pytest.fixture
def auth_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def note(user):
    return NoteFactory(user=user)


@pytest.fixture
def another_note(another_user):
    return NoteFactory(user=another_user)


@pytest.fixture
def category():
    return CategoriesFactory()


@pytest.fixture
def category_with_note(category, note):
    category.notes.add(note)
    return category
