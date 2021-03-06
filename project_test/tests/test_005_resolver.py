# -*- coding: utf-8 -*-
import pytest

from django.core.urlresolvers import reverse

from autobreadcrumbs.resolver import PathBreadcrumbResolver

# Autodiscovering is disabled since it allready have be executed
# previously, see warning from "test_004_autodiscover.py"
# from autobreadcrumbs.discover import autodiscover
# autodiscover()


@pytest.mark.parametrize("path,segments", [
    ('/foo/', [
        '/',
        '/foo/',
    ]),
    ('foo/', [
        '/',
        '/foo/',
    ]),
    ('/foo', [
        '/',
        '/foo/',
    ]),
     (u'/télô/你好/', [
        '/',
        u'/télô/',
        u'/télô/你好/',
    ]),
    ('/foo/bar/', [
        '/',
        '/foo/',
        '/foo/bar/',
    ]),
    ('/foo/bar-mip/flop/', [
        '/',
        '/foo/',
        '/foo/bar-mip/',
        '/foo/bar-mip/flop/',
    ]),
    ('/foo/bar/foo/zouip/', [
        '/',
        '/foo/',
        '/foo/bar/',
        '/foo/bar/foo/',
        '/foo/bar/foo/zouip/',
    ]),
])
def test_cut_path_into_segments(settings, path, segments):
    """Cut a path into segments"""
    resolver = PathBreadcrumbResolver(settings.ROOT_URLCONF)

    assert resolver.cut(path) == segments


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
    (
        '/foo/invisible/chu/',
        'Chu',
        ['Home', 'Foo', 'Chu']
    ),
    (
        '/foo/sluggy/plaf/',
        'Sluggy',
        ['Home', 'Foo', 'Sluggy']
    ),
    (
        '/foo/date/2016/08/',
        'Year month',
        ['Home', 'Foo', "Year month"]
    ),
    (
        '/foo/sub/plop/',
        'Plop',
        ['Home', 'Foo', 'Sub', 'Plop']
    ),
    (
        '/foo/controlled-true/yep/',
        'Control Yep',
        ['Home', 'Foo', 'Controlled true', 'Control Yep']
    ),
    (
        '/foo/controlled-false/nope/',
        'Control Nope',
        ['Home', 'Foo', 'Control Nope']
    ),
])
def test_resolving_path(settings, rf, url, urlcurrent, urltitles):
    """Resolve breadcrumbs from a path"""
    # Forge a request object from url
    request = rf.get(url)
    resolver = PathBreadcrumbResolver(settings.ROOT_URLCONF)
    results = resolver.resolve(request.path, request=request)

    elements = results['autobreadcrumbs_elements']
    current = results['autobreadcrumbs_current']

    #print [str(item.title) for item in elements]

    assert [item.title for item in elements] == urltitles

    assert current.title == urlcurrent
