import pytest
from django.urls import reverse
from django.conf import settings

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('creat_news')
def test_news_order(client):
    url = reverse('news:home')
    reader = client.get(url)
    object_list = reader.context['object_list']
    sorted_news = sorted(object_list, key=lambda news: news.date, reverse=True)
    for a, b in zip(object_list, sorted_news):
        assert a.date == b.date


@pytest.mark.usefixtures('creat_comments')
def test_comments_order(client, pk_news):
    url = reverse('news:detail', args=pk_news)
    reader = client.get(url)
    object_list = reader.context['news'].comment_set.all()
    sorted_comments = sorted(object_list, key=lambda comment: comment.created)
    for a, b in zip(object_list, sorted_comments):
        assert a.created == b.created


@pytest.mark.usefixtures('creat_news')
def test_news_count(client):
    url = reverse('news:home')
    reader = client.get(url)
    object_list = reader.context['object_list']
    comments_count = len(object_list)
    assert comments_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.parametrize('username, is_permitted',
                         ((pytest.lazy_fixture('admin_client'), True),
                          (pytest.lazy_fixture('client'), False)))
def test_comment_form_availability_for_different_users(
        pk_news, username, is_permitted):
    url = reverse('news:detail', args=pk_news)
    reader = username.get(url)
    result = 'form' in reader.context
    assert result == is_permitted
