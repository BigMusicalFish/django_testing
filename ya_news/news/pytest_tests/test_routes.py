from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'page, args',
    (('news:home', None),
     ('users:login', None),
     ('users:logout', None),
     ('users:signup', None),
     ('news:detail', pytest.lazy_fixture('pk_news')),),
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, page, args):
    '''Главная страница, страница отдельной новости, страницы регистрации,
    входа и выхода из учетной записи доступны анонимному пользователю'''
    url = reverse(page, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page, args',
    (('news:edit', pytest.lazy_fixture('pk_comment')),
     ('news:delete', pytest.lazy_fixture('pk_comment')),),
)
def test_pages_availability_for_auth_user(author_client, page, args):
    '''Страницы редактирования и удаления комментария доступны его автору'''
    url = reverse(page, args=args)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page, args',
    (('news:edit', pytest.lazy_fixture('pk_comment')),
     ('news:delete', pytest.lazy_fixture('pk_comment')),),
)
def test_redirects(client, page, args):
    '''При попытке редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации'''
    login_url = reverse('users:login')
    url = reverse(page, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize('page', ('news:edit', 'news:delete'))
def test_pages_availability_for_different_users(page, pk_comment,
                                                admin_client):
    '''При попытке редактирования или удаления
    комментария не автором, возвращается ошибка'''
    url = reverse(page, args=pk_comment)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
