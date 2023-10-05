from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.models import Comment, News
from news.forms import BAD_WORDS, WARNING

import pytest


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def comment(author):
    comment = Comment.objects.create(
        text='Текст комментария',
        author=author,
    )
    return comment


@pytest.fixture
def news(author):
    comment = News.objects.create(
        text='Текст новости',
        author=author,
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


def test_user_can_create_comment(author_client, author, form_data):
    url = reverse('news:detail')
    response = author_client.post(url, data=form_data)
    assertRedirects(response, reverse('news:detail'))
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data):
    url = reverse('news:detail')
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id))
    response = author_client.post(url, form_data)
    assertRedirects(response, reverse('news:detail'))
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(admin_client, form_data, comment):
    url = reverse('notes:edit', args=(comment.id))
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_user_cant_use_bad_words(author_client):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    comments_count = Comment.objects.count()
    assert comments_count == 0
