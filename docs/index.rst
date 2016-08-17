.. Boussole documentation master file, created by
   sphinx-quickstart on Sun Mar  6 12:12:38 2016.

.. _breadcrumbs: http://en.wikipedia.org/wiki/Breadcrumb_%28navigation%29#Websites
.. _Django: https://www.djangoproject.com/

Welcome to AutoBreadcrumbs's documentation!
===========================================

This is a Django application to automatically build `breadcrumbs`_ like this : ::

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

User’s Guide
************

.. toctree::
   :maxdepth: 2

   install.rst
   overview.rst
   library_references/settings.rst
   library_references/templatetags.rst

Developer’s Guide
*****************

.. toctree::
   :maxdepth: 2

   library_references/registry.rst
   library_references/discover.rst
   library_references/resolver.rst
   library_references/context_processors.rst
   development.rst
   changelog.rst
