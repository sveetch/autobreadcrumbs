import pytest

from autobreadcrumbs.discover import autodiscover


def test_registry_autodiscover(client):
    """Check registred crumb names after autodiscover"""
    from autobreadcrumbs.registry import breadcrumbs_registry

    autodiscover()

    assert breadcrumbs_registry.get_names() == [
        'bar',
        'bar-ometer',
        'foo:index',
        'foo:invisible',
        'foo:invisible-chu',
        'foo:pika',
        'foo:pika-chu',
        'foo:slug',
        'foo:subfoo:index',
        'foo:subfoo:plop',
        'foo:year-month',
        'homepage',
    ]
