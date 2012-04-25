# -*- coding: utf-8 -*-
"""
App default settings and autodiscover
"""
from django.conf import settings

from autobreadcrumbs.sites import BreadcrumbSite, site

# HTML template string used in tag ``{% autobreadcrumbs_links %}``
AUTOBREADCRUMBS_HTML_LINK = getattr(settings, 'AUTOBREADCRUMBS_HTML_LINK', u'<a href="/{link}">{title}</a>')
AUTOBREADCRUMBS_HTML_SEPARATOR = getattr(settings, 'AUTOBREADCRUMBS_HTML_SEPARATOR', u' &gt; ')

# ACTION_CHECKBOX_NAME is unused, but should stay since its import from here
# has been referenced in documentation.

def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.crumbs' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            # (see #8245).
            site._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'crumbs'):
                raise
