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
        author=author,
    )
    return comment


@pytest.fixture
def news(author):
    comment = News.objects.create(
        text='Текст комментария',
        author=author,
    )
    return comment


def form_data():
    return {
        'text': 'Новый текст',
    }
