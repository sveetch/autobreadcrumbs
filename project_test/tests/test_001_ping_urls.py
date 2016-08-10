"""
Some dummy pinging to ensure urls are consistent

WARNING: Keep this syncrhonized with enabled urls files
"""
import pytest

from django.core.urlresolvers import reverse


@pytest.mark.parametrize("url_name,url_args,url_kwargs", [
    ('home', [], {}),
    ('foo:index', [], {}),
    ('foo:pika', [], {}),
    ('foo:pika-chu', [], {}),
    ('foo:subfoo:index', [], {}),
    ('foo:subfoo:plop', [], {}),
    ('foo:slug', ['plop'], {}),
    ('foo:year-month', [], {'year':2016, 'month': '08'}),
    ('foo:invisible', [], {}),
    ('foo:invisible-chu', [], {}),
    ('bar', [], {}),
    ('bar-ometer', [], {}),
])
def test_ping_reverse_urlname(client, url_name, url_args, url_kwargs):
    """Ping reversed url names"""
    response = client.get(reverse(url_name, args=url_args, kwargs=url_kwargs))
    assert response.status_code == 200


@pytest.mark.parametrize("url", [
    '/',
    '/foo/',
    '/foo/pika/',
    '/foo/pika/chu/',
    '/foo/sub/',
    '/foo/date/2016/08/',
    '/foo/sluggy/plop/',
    '/foo/sub/plop/',
    '/foo/invisible/',
    '/foo/invisible/chu/',
    '/bar/',
    '/bar/ometer/',
])
def test_ping_url(client, url):
    """Ping reversed url names"""
    response = client.get(url)
    assert response.status_code == 200
