from django.urls import reverse

import pytest


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('id')),
        ('news:edit', pytest.lazy_fixture('id'))
    )
)
def test_anonymous_client_has_no_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.post(url, data=form_data)
    assert 'form' in response.context


def test_anonymous_client_has_no_form(client, name, args):
    url = reverse(name, args=args)
    response = client.post(url, data=form_data)
    assert 'form' not in response.context
