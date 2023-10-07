from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(author=cls.author, title='Заголовок',
                                       text='Текст заметки', slug='slug')

    def test_pages_contains_form(self):
        urls = (('notes:add', None), ('notes:edit', self.note.slug))
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                self.client.force_login(self.author)
                response = self.client.get(url)
                self.assertIn('form', response.context)

    def test_notes_list_for_different_users(self):
        notes = ((self.author, True), (self.reader, False))
        url = reverse('notes:list')
        for user, note_list in notes:
            self.client.force_login(user)
            with self.subTest(user=user.username, note_list=note_list):
                response = self.client.get(url)
                object_list = self.note in response.context['object_list']
                self.assertEqual(object_list, note_list)
