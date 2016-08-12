# -*- coding: utf-8 -*-
"""
Template context processor
==========================

"""
from django.conf import settings

#from autobreadcrumbs.resolver import PathBreadcrumbResolver

def AutoBreadcrumbsContext(request):
    """
    Context processor to find breadcrumbs from current ressource

    Use ``request.path`` to know the path from which to find the breadcrumbs, cut the
    path in segments and check each of them to find breadcrumb details if any.
    """
    #return PathBreadcrumbResolver(request)
    return {}
