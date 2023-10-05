from django.urls import reverse

import pytest

from news.models import Comment, News

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
        author=author)
    return comment


@pytest.fixture
def news(author):
    comment = News.objects.create(
        text='Текст новости',
        author=author)
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст',
    }


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('id')),
        ('news:edit', pytest.lazy_fixture('id'))
    )
)
def test_anonymous_client_has_no_form(author_client, form_data, name, args):
    url = reverse(name, args=args)
    response = author_client.post(url, data=form_data)
    assert 'form' in response.context


def test_anonymous_client_has_no_form(client, form_data, name, args):
    url = reverse(name, args=args)
    response = client.post(url, data=form_data)
    assert 'form' not in response.context


def test_news_count(author_client):
    url = reverse('news:home')
    response = author_client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == 10
