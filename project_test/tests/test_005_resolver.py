import pytest

from django.core.urlresolvers import reverse

from autobreadcrumbs.resolver import PathBreadcrumbResolver
from autobreadcrumbs.discover import autodiscover

def test_check_breadcrumb_site(rf):
    """..."""
    autodiscover()

    url = reverse('foo:year-month', kwargs={'year':2016, 'month': '08'})
    request = rf.get(url)
    print PathBreadcrumbResolver(request)

    #Should not be empty when crumbs will be registred in 'project_test'
    assert 1 == 42
