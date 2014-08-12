# -*- coding: utf-8 -*-
"""
Context Processor

NOTE: Actually this is doing a resolving on each part of url at each request.
      I think this is not the better for performance, resolving possibility should be 
      cached at discovering, but HOW TO PROCEED ?
"""
from django.conf import settings
from django.core.urlresolvers import Resolver404, get_resolver

from autobreadcrumbs import site

def AutoBreadcrumbsContext(request):
    """
    Context processor to find breadcrumbs from current ressource
    
    Use ``request.path`` to know the path from which to find the breadcrumbs, cut the 
    path in segments and check each of them to find breadcrumb details if any.
    """
    relative_url = request.path
    urlresolver = get_resolver(settings.ROOT_URLCONF)
    breadcrumbs_elements = []
    current = None
    
    # Cut the path in segments
    # For ``/foo/bar/`` it will give :
    #      - /
    #      - /foo
    #      - /foo/bar
    path_segments = ['/']
    tmp = '/'
    for segment in relative_url.split('/'):
        if segment:
            tmp += segment+'/'
            path_segments.append(tmp)
    
    # Resolve each segment
    for seg in path_segments:
        try:
            resolved = urlresolver.resolve(seg)
        except Resolver404:
            pass
        else:
            view_control = None
            namespace = resolved.namespace
            title = name = resolved.url_name
            
            if hasattr(resolved.func, "crumb_hided"):
                continue
            
            if namespace:
                name = ':'.join([namespace, name])
                
            if hasattr(settings, "AUTOBREADCRUMBS_TITLES") and name in getattr(settings, "AUTOBREADCRUMBS_TITLES", {}):
                title = settings.AUTOBREADCRUMBS_TITLES[title]
            elif site.has_title(name):
                title = site.get_title(name)
            else:
                continue
            
            if title is None:
                continue
            
            # Force unicode on lazy translation else it will trigger an exception with 
            # templates
            if hasattr(title, '_proxy____unicode_cast'):
                title = unicode(title)
            # Value with tuple should contain a title and a simple method to control 
            # access (return ``True`` for granted access and ``False`` for forbidden 
            # access
            elif isinstance(title, tuple) or isinstance(title, list):
                title, view_control = title
                if not view_control(name, request):
                    continue
            
            # Finally append the part to the knowed crumbs list
            breadcrumbs_elements.append( BreadcrumbRessource(seg, name, title, resolved.args, resolved.kwargs) )
        
    if len(breadcrumbs_elements)>0:
        current = breadcrumbs_elements[-1]
    
    return {
        'autobreadcrumbs_elements': breadcrumbs_elements,
        'autobreadcrumbs_current': current,
    }

class BreadcrumbRessource(object):
    def __init__(self, path, name, title, view_args, view_kwargs):
        self.path = path
        self.name = name
        self.title = title
        self.view_args = view_args
        self.view_kwargs = view_kwargs
        
    def __repr__(self):
        return "<BreadcrumbRessource: {0}>".format(self.name)
        
    def __str__(self):
        # NOTE: should be __unicode__() because passed paths can be unicode... right ?
        return self.path
