# -*- coding: utf-8 -*-
"""
Settings
========

"""
#: Initial project crumbs where you can add initial crumbs for your project
#: views.
AUTOBREADCRUMBS_TITLES = {}

#: Optional project level crumbs file, this have to be a correct Python path to
#: a crumb module.
AUTOBREADCRUMBS_ROOT_CRUMB = None

#: Template string for crumb item in tag ``{% autobreadcrumbs_links %}``
AUTOBREADCRUMBS_HTML_LINK = u'<a href="{link}">{title}</a>'

#: Template string for separator item in tag ``{% autobreadcrumbs_links %}``
AUTOBREADCRUMBS_HTML_SEPARATOR = u' &gt; '
