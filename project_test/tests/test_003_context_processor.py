import pytest

from django.core.urlresolvers import reverse

def test_check_breadcrumb_site(rf):
    """..."""
    from autobreadcrumbs.context_processors import AutoBreadcrumbsContext
    url = reverse('foo:year-month', kwargs={'year':2016, 'month': '08'})
    request = rf.get(url)
    print AutoBreadcrumbsContext(request)

    # Should not be empty when crumbs will be registred in 'project_test'
    #assert 1 == 42
