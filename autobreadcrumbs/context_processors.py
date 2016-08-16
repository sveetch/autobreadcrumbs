# -*- coding: utf-8 -*-
"""
Template context processor
==========================

"""
from django.conf import settings

from autobreadcrumbs.resolver import PathBreadcrumbResolver


def AutoBreadcrumbsContext(request):
    """
    Context processor to resolve breadcrumbs from current ressource.

    Use ``request.path`` to know the current ressource url path and
    ``settings.ROOT_URLCONF`` to resolve it.
    """
    r = PathBreadcrumbResolver(settings.ROOT_URLCONF)
    return r.resolve(request.path, request=request)
