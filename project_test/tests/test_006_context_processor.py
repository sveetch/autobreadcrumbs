# -*- coding: utf-8 -*-
import pytest

from autobreadcrumbs.context_processors import AutoBreadcrumbsContext

@pytest.mark.parametrize("url,urlcurrent,urltitles", [
    (
        '/',
        'Home',
        ['Home']
    ),
    (
        '/bar/',
        'Bar',
        ['Home', 'Bar']
    ),
])
def test_context(rf, url, urlcurrent, urltitles):
    """Test context_processor"""
    request = rf.get(url)

    context = AutoBreadcrumbsContext(request)

    #print dir(request)
    elements = context['autobreadcrumbs_elements']
    current = context['autobreadcrumbs_current']

    assert [item.title for item in elements] == urltitles

    assert current.title == urlcurrent
