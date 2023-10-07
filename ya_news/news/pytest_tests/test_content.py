import pytest
from django.urls import reverse
from django.conf import settings

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('create_news')
def test_news_order(client):
    url = reverse('news:home')
    res = client.get(url)
    object_list = res.context['object_list']
    sorted_news = sorted(object_list,
                         key=lambda news: news.date,
                         reverse=True)
    for as_is, to_be in zip(object_list, sorted_news):
        assert as_is.date == to_be.date


@pytest.mark.usefixtures('create_comments')
def test_comments_order(client, pk_news):
    url = reverse('news:detail', args=pk_news)
    res = client.get(url)
    object_list = res.context['news'].comment_set.all()
    sorted_comments = sorted(object_list,
                             key=lambda comment: comment.created)
    for as_is, to_be in zip(object_list, sorted_comments):
        assert as_is.created == to_be.created


@pytest.mark.usefixtures('create_comments')
def test_news_count(client):
    url = reverse('news:home')
    res = client.get(url)
    object_list = res.context['object_list']
    comments_count = len(object_list)
    assert comments_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.parametrize('username, is_permitted',
                         ((pytest.lazy_fixture('admin_client'), True),
                          (pytest.lazy_fixture('client'), False)))
def test_comment_form_availability_for_different_users(
        pk_news, username, is_permitted):
    url = reverse('news:detail', args=pk_news)
    res = username.get(url)
    result = 'form' in res.context
    assert result == is_permitted
