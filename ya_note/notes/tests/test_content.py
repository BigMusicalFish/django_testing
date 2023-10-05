from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    HOME_URL = reverse('notes:home')

    @classmethod
    def setUpTestData(cls):
        cls.notes = Note.objects.create(title='Заголовок', text='Текст')
        cls.author = User.objects.create(username='Автор')
        cls.admin = User.objects.create(username='Админ')
        all_notes = [
            Note(title=f'Заметка {index}', text='Текст заметки.')
            for index in range(settings.NOTE_COUNT_ON_HOME_PAGE + 1)
        ]
        Note.objects.bulk_create(all_notes)

    def test_note_in_list_for_author(self):
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        self.assertIn(self.notes, object_list)

    def test_note_not_in_list_for_another_user(self):
        url = reverse('notes:list')
        response = self.admin.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.notes, object_list)

    def test_create_note_page_contains_form(self):
        url = reverse('notes:add')
        response = self.author.get(url)
        self.assertIn('form', response.context)
