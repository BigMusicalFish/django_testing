from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from django.urls import reverse

import pytest


@pytest.mark.parametrize('name', ('news:home', 'news:detail',
                                  'users:logout', 'users:login',
                                  'users:signup'))
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_cjmments_availability_for_author(author_client, name, comment):
    url = reverse(name, args=(comment.slug,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, comment_object',
    (
        ('news:edit', pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('comment')),
    ),
)
def test_redirects(client, name, comment_object):
    login_url = reverse('users:login')
    if comment_object is not None:
        url = reverse(name, args=(comment_object.slug,))
    else:
        url = reverse(name)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        ('admin_client', HTTPStatus.NOT_FOUND),
        ('author_client', HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_cjmments_availability_for_different_users(
        parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
