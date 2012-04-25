# -*- coding: utf-8 -*-
from django.conf import settings

from autobreadcrumbs.sites import BreadcrumbSite, site

# HTML template string used in tag ``{% autobreadcrumbs_links %}``
AUTOBREADCRUMBS_HTML_LINK = getattr(settings, 'AUTOBREADCRUMBS_HTML_LINK', u'<a href="/{link}">{title}</a>')
AUTOBREADCRUMBS_HTML_SEPARATOR = getattr(settings, 'AUTOBREADCRUMBS_HTML_SEPARATOR', u' &gt; ')
