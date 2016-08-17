# -*- coding: utf-8 -*-
"""
Template tags
=============

Every template tag render crumb title using template syntax with given context
(from your view), so you can use something like ``{{ myvar }}`` in a title for
a view which have the ``myvar`` variable available in its context. This means
template blocks and filters can be used also.

Note:
    Template tags require some variable inside Template context that are
    injected from context processor
    ``autobreadcrumbs.context_processors.AutoBreadcrumbsContext``. So you
    either have to enabled it in your template context processors or inject
    them from your views.
"""
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe


register = template.Library()


class CurrentWalkthroughRender(template.Node):
    """
    Tag node render for ``currentwalkthroughto``.
    """
    def __init__(self, nodelist, urlname):
        self.nodelist = nodelist
        self.urlname = urlname

    def render(self, context):
        output = self.nodelist.render(context)
        urlname = template.resolve_variable(self.urlname, context)

        if 'autobreadcrumbs_elements' in context:
            if len(filter(lambda x: (x.name == urlname),
                          context['autobreadcrumbs_elements'])):
                return output

        return ''


@register.tag
def currentwalkthroughto(parser, token):
    """
    Template tag to output content if current ressource walk through given
    url name.

    Example:
        Template tag take one requirement argument ``name`` that is an url name
        to search for in breadcrumbs, if the current ressource crumb walk
        through it, content inside tag will be rendered: ::

            {% load autobreadcrumb %}
            {% currentwalkthroughto 'bar' %}Hello{% endcurrentwalkthroughto %}
    """
    nodelist = parser.parse(('endcurrentwalkthroughto',))
    parser.delete_first_token()

    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(("You need to specify an url name "
                                            "to compare with"))
    else:
        return CurrentWalkthroughRender(nodelist, *args[1:])


@register.simple_tag(takes_context=True)
def current_title_from_breadcrumbs(context):
    """
    Template tag to output breadcrumb title from current ressource crumb.

    Example:
        ::

            {% load autobreadcrumb %}
            {% current_title_from_breadcrumbs %}
    """
    if context.get('autobreadcrumbs_current', False):
        tpl = template.Template(context['autobreadcrumbs_current'].title)
        return tpl.render(template.Context(context))

    return ''


@register.inclusion_tag('autobreadcrumbs_tag.html', takes_context=True)
def autobreadcrumbs_tag(context):
    """
    Template tag to output HTML for full breadcrumbs using template
    ``autobreadcrumbs_tag.html``.

    Example:
        ::

            {% load autobreadcrumb %}
            {% autobreadcrumbs_tag %}
    """
    if 'autobreadcrumbs_elements' in context:
        elements = []
        for item in context['autobreadcrumbs_elements']:
            tpl = template.Template(item.title)
            title = tpl.render(template.Context(context))

            elements.append(dict(zip(
                (
                    'url', 'title', 'name',
                    'view_args', 'view_kwargs'
                ),
                (
                    item.path, title, item.name,
                    item.view_args, item.view_kwargs
                )
            )))
        return {'elements': elements}

    return {}


@register.simple_tag(takes_context=True)
def autobreadcrumbs_links(context):
    """
    Template tag which use ``AUTOBREADCRUMBS_HTML_LINK`` and
    ``AUTOBREADCRUMBS_HTML_SEPARATOR`` settings to build a HTML list of
    breadcrumbs.

    Returned HTML is marked as safe (not to escape) for templates.

    Example:
        ::

            {% load autobreadcrumb %}
            {% autobreadcrumbs_links %}
    """
    if 'autobreadcrumbs_elements' in context:
        elements = []
        html_link = settings.AUTOBREADCRUMBS_HTML_LINK
        html_separator = settings.AUTOBREADCRUMBS_HTML_SEPARATOR

        for item in context['autobreadcrumbs_elements']:
            tpl = template.Template(item.title)
            title = tpl.render(template.Context(context))
            elements.append(html_link.format(link=item.path, title=title))

        return mark_safe(html_separator.join(elements))

    return ''

autobreadcrumbs_links.is_safe = True
