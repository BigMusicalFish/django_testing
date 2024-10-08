from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    '''Тестирует пути'''

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_pages_availability_for_anonymous_user(self):
        '''Главная страница, страницы регистрации, входа и
        выхода из учетной записи доступны анонимному пользователю'''
        urls = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        for page in urls:
            with self.subTest(page=page):
                url = reverse(page)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        '''Страницы со списком заметок, успешного добавления заметки
        и добавления новой заметки доступна зарегистрированному пользователю'''
        urls = (
            'notes:list',
            'notes:success',
            'notes:add',
        )
        self.client.force_login(self.author)
        for page in urls:
            with self.subTest(page=page):
                url = reverse(page)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_create_edit_and_delete(self):
        '''Страницы отдельной заметки, редактирования
        и удаления заметки доступны автору заметки'''
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for page in ('notes:detail', 'notes:edit', 'notes:delete'):
                with self.subTest(user=user.username, page=page):
                    url = reverse(page, args=[self.note.slug])
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        '''При переходе на страницу заметок, страницы успешного
        добавления записи, добавления заметки, отдельной заметки,
        редактирования или удаления заметки аноним перенаправляется
        на страницу авторизации'''
        login_url = reverse('users:login')
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
