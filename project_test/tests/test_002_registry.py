import pytest

from django.core.urlresolvers import reverse

def test_check_breadcrumb_site(client):
    """Just pinging dummy homepage"""
    from autobreadcrumbs.sites import site
    from autobreadcrumbs.sites import BreadcrumbSite

    # Should not be empty when crumbs will be registred in 'project_test'
    # NOTE: registry don't watch at settings.AUTOBREADCRUMBS_TITLES, only
    # resolver (ag: the context processor) use it, it's a BAD behavior
    assert site.get_registry().keys() == [
        'foo:subfoo:index',
        'foo:index',
        'foo:invisible',
        'foo:pika',
        'foo:subfoo:plop',
        'foo:year-month',
        'foo:pika-chu',
        'foo:slug',
        'foo:invisible-chu',
    ]


# NOTE: overriding with pytest.mark.urls does not seem to work as autodiscover
#     still be used
#@pytest.mark.urls('project.urls_no_autodiscover')
#def test_check_breadcrumb_site_empty(client):
    #"""Just pinging dummy homepage"""
    #from autobreadcrumbs.sites import site
    #from autobreadcrumbs.sites import BreadcrumbSite

    #assert site.get_registry() == BreadcrumbSite().get_registry()
