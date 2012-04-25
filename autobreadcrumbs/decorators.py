# -*- coding: utf-8 -*-
"""
Decorator to push breadcrumb values on views

This will useless since Django 1.3 where we start to migrate to *Class based views* 
which is not very easy to decorate properly. In the same reasons, these decorators doesn't 
works with *Form Wizards*.

DEPRECATED
"""
def autobreadcrumb_add(value):
    """
    Add breadcrumb entry to a view
    
    * Un string, dans ce cas il est définit comme l'unique titre possible de la vue
    * Un dictionnaire, indexé sur le nom des url (tel que définit dans les "urls.py") 
      contenant les titres possibles selon l'url qui l'apelle
    """
    def _set_var(obj):
        if isinstance(value, basestring):
            setattr(obj, "crumb_title", value)
        elif isinstance(value, dict):
            setattr(obj, "crumb_titles", value)
        return obj
    return _set_var

def autobreadcrumb_hide(value):
    """
    Hide a view from breadcrumbs
    
    Actuellement il faut utiliser le décorateur de la façon suivante : ::
            
        @autobreadcrumb_hide('')
        def mafonction(foo):
            ..
    
    """
    def _set_var(obj):
        setattr(obj, "crumb_hided", True)
        return obj
    return _set_var
