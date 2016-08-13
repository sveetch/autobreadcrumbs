# -*- coding: utf-8 -*-
"""
Breadcrumb resolving
====================

NOTE: Actually this is doing a resolving on each part of url at each request.
      I think this is not the better for performance, resolving possibility
      should be cached at discovering, but HOW TO PROCEED ?
"""
from django.conf import settings
from django.core.urlresolvers import Resolver404, get_resolver

from autobreadcrumbs.registry import breadcrumbs_registry


class BreadcrumbRessource(object):
    """
    Simple crumb ressource model to contain all datas about a ressource.
    """
    def __init__(self, path, name, title, view_args, view_kwargs):
        self.path = path
        self.name = name
        self.title = title
        self.view_args = view_args
        self.view_kwargs = view_kwargs

    def __repr__(self):
        return "<BreadcrumbRessource: {0}>".format(self.name)

    def __str__(self):
        # NOTE: should be __unicode__() because passed paths can be unicode...
        # right ?
        return self.path


class PathBreadcrumbResolver(object):
    """
    Resolve given path as breadcrumbs

    Arguments:
        root_urlconf (string): Python path to an url conf file, usually
            ``settings.ROOT_URLCONF``. It will be used as the url map to
            resolve every given path.
    """
    def __init__(self, root_urlconf):
        self.urlresolver = get_resolver(root_urlconf)

    def cut(self, path):
        """
        Cut given path into segments

        Arguments:
            path (string): An url path like ``/foo/bar/``.

        Returns:
            list: List of path segments, each segment is a part of the url path
            starting from ``/`` and ending on the full path.

            Such as for ``/foo/bar/`` segments will be: ::

                - /
                - /foo
                - /foo/bar

        """
        # Cut the path in segments
        segments = ['/']
        tmp = '/'
        for item in path.split('/'):
            if item:
                tmp += item + '/'
                segments.append(tmp)

        return segments

    def format_title(self, name, value, request=None):
        """
        Manage title format

        Arguments:
            name (string): Url name.
            value (string or tuple): Crumb value for defined url name.
                Can be a simple string, or a Django lazy unicode or a tuple
                ``(title, custom_function)``.

                ``custom_function`` take url name
                and request object as arguments and will return ``False`` to
                ignore crumb (won't be in breadcrumbs) or ``True`` to keep
                crumb element.

        Keyword Arguments:
            request (django.http.request.HttpRequest): Optional Django request
                object used with custom crumb function. If not given, crumb
                functions is ignored (so the crumb ressource still be
                available).

        Returns:
            string: Crumb title.
        """
        title = value

        if value is None:
            return None

        # Force unicode on lazy translation else it will trigger an exception
        # with templates
        if hasattr(value, '_proxy____unicode_cast'):
            title = unicode(value)
        # Custom function usage
        elif (isinstance(value, tuple) or isinstance(value, list)) and request:
            title, view_control = value
            if not view_control(name, request):
                return None

        return title

    def get_current(self, elements):
        """
        Return current Breadcrumb from elements.

        This is pretty simple as the current element is allways the last
        element (if element list is not empty).

        Arguments:
            elements (list): List of breadcrumb elements.

        Returns:
            BreadcrumbRessource: The last element from given ``elements`` if
                any, else None.
        """
        if len(elements)>0:
            return elements[-1]

        return None

    def resolve(self, path, request=None):
        """
        Return resolved breadcrumbs datas from given path.

        Cut the path in segments and check each of them to find breadcrumb
        details if any.

        Arguments:
            path (string): An url path like ``/foo/bar/``.

        Keyword Arguments:
            request (Django request object): Optional request object that will
                be given to eventual view control functions.

        Returns:
            Dict: Datas from resolved crumbs:

            * ``autobreadcrumbs_elements``: Resolved bread crumbs for each
              segment;
            * ``autobreadcrumbs_current``: Breadcrumb for current (the last
              one) path.

        """
        breadcrumbs_elements = []

        path_segments = self.cut(path)

        # Resolve each segment
        for seg in path_segments:
            try:
                resolved = self.urlresolver.resolve(seg)
            except Resolver404:
                pass
            else:
                view_control = None
                namespace = resolved.namespace
                title = name = resolved.url_name

                if namespace:
                    name = ':'.join([namespace, name])

                # Ignore ressource without a crumb title
                if not breadcrumbs_registry.has_title(name):
                    continue

                # Get defined title
                title = breadcrumbs_registry.get_title(name)
                title = self.format_title(name, title, request=request)
                # Ignore element if empty
                if title is None:
                    continue

                # Finally append the part to the knowed crumbs list
                breadcrumbs_elements.append(
                    BreadcrumbRessource(seg, name, title, resolved.args,
                                        resolved.kwargs)
                )

        return {
            'autobreadcrumbs_elements': breadcrumbs_elements,
            'autobreadcrumbs_current': self.get_current(breadcrumbs_elements),
        }
