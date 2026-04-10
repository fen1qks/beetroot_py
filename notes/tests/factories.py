import factory
from django.contrib.auth.models import User

from ..models import Note, Categories


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        raw_password = extracted or 'testpass123'
        self.set_password(raw_password)
        if create:
            self.save()


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'Нотатка {n}')
    text = factory.Faker('sentence', nb_words=6)
    reminder = False
    is_done = False


class CategoriesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories

    name_categories = factory.Sequence(lambda n: f'Категорія {n}')

    @factory.post_generation
    def notes(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for note in extracted:
                self.notes.add(note)