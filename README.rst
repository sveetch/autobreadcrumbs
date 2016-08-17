.. _breadcrumb: http://en.wikipedia.org/wiki/Breadcrumb_%28navigation%29#Websites
.. _Django: https://www.djangoproject.com/

===============
Autobreadcrumbs
===============

This is a Django application to automatically build breadcrumbs like this : ::

  Home > Some page > Some child page

Each *crumb* displays a title with a link to represent a view, crumb tree is
determined from the urls map of your project, crumbs are linked to view url
name (including namespaces).

Links
*****

* Read the documentation on `Read the docs <http://autobreadcrumbs.readthedocs.io/>`_;
* Download its `PyPi package <https://pypi.python.org/pypi/autobreadcrumbs>`_;
* Clone it on its `Github repository <https://github.com/sveetch/autobreadcrumbs>`_;

Dependancies
************

* `Django`_ >= 1.6;
