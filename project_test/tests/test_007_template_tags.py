# -*- coding: utf-8 -*-
import pytest

from django.template import Context, Template

from autobreadcrumbs.context_processors import AutoBreadcrumbsContext


@pytest.mark.parametrize("url,title", [
    ('/', 'Home'),
    ('/foo/', 'Foo'),
    ('/foo/date/2016/08/', 'Year month'),
    ('/foo/sub/plop/', 'Plop'),
])
def test_current_title_from_breadcrumbs(rf, url, title):
    """Render 'current_title_from_breadcrumbs' tag"""
    template = ("{% load autobreadcrumb %}"
                "{% current_title_from_breadcrumbs %}")

    # Render template with context filled from context processor just as it
    # would be within a common view
    request = rf.get(url)
    context = Context()
    context.update(AutoBreadcrumbsContext(request))
    t = Template(template)
    output = t.render(context)

    assert output == title


@pytest.mark.parametrize("url,crossing,attempt", [
    ('/', 'home', 'Yep'),
    ('/foo/', 'foo:index', 'Yep'),
    ('/foo/', 'bar', ''),
    ('/foo/date/2016/08/', 'foo:index', 'Yep'),
    ('/foo/sub/plop/', 'foo:subfoo:index', 'Yep'),
])
def test_currentwalkthroughto(rf, url, crossing, attempt):
    """Render 'currentwalkthroughto' tag"""
    template = ("{{% load autobreadcrumb %}}"
                "{{% currentwalkthroughto '{crossing}' %}}Yep"
                "{{% endcurrentwalkthroughto %}}")

    # Render template with context filled from context processor just as it
    # would be within a common view
    request = rf.get(url)
    context = Context()
    context.update(AutoBreadcrumbsContext(request))
    t = Template(template.format(crossing=crossing))
    output = t.render(context)

    assert output == attempt


@pytest.mark.parametrize("url,attempt", [
    (
        "/",
        ("""<p id="breadcrumbs">"""
        """<a href="/">Home</a>"""
        """</p>""")
    ),
    (
        "/foo/sub/plop/",
        ("""<p id="breadcrumbs">"""
        """<a href="/">Home</a>"""
        """ &gt; """
        """<a href="/foo/">Foo</a>"""
        """ &gt; """
        """<a href="/foo/sub/">Sub</a>"""
        """ &gt; """
        """<a href="/foo/sub/plop/">Plop</a>"""
        """</p>""")
    ),
])
def test_autobreadcrumbs_tag(rf, url, attempt):
    """Render 'autobreadcrumbs_tag' tag"""
    template = ("{% load autobreadcrumb %}"
                "{% autobreadcrumbs_tag %}")

    # Render template with context filled from context processor just as it
    # would be within a common view
    request = rf.get(url)
    context = Context()
    context.update(AutoBreadcrumbsContext(request))
    t = Template(template)
    output = t.render(context)

    assert output == attempt


@pytest.mark.parametrize("url,attempt", [
    (
        "/",
        """<a href="/">Home</a>"""
    ),
    (
        "/foo/sub/plop/",
        ("""<a href="/">Home</a>"""
        """ &gt; """
        """<a href="/foo/">Foo</a>"""
        """ &gt; """
        """<a href="/foo/sub/">Sub</a>"""
        """ &gt; """
        """<a href="/foo/sub/plop/">Plop</a>""")
    ),
])
def test_autobreadcrumbs_links(rf, url, attempt):
    """Render 'autobreadcrumbs_links' tag"""
    template = ("{% load autobreadcrumb %}"
                "{% autobreadcrumbs_links %}")

    # Render template with context filled from context processor just as it
    # would be within a common view
    request = rf.get(url)
    context = Context()
    context.update(AutoBreadcrumbsContext(request))
    t = Template(template)
    output = t.render(context)

    assert output == attempt
