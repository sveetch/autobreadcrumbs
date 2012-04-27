.. _breadcrumb: http://en.wikipedia.org/wiki/Breadcrumb_%28navigation%29#Websites
.. _Django internationalization system: https://docs.djangoproject.com/en/dev/topics/i18n/

Introduction
============

**AutoBreadcrumbs** is a Django application to automatically build a breadcrumb in your website like 
this : ::

  Home > Some page > Some child page

Each *crumb* displays a title with a link to represent a view, the crumb tree is determined from the urls map 
of your project, their titles and links are determined from the associated view entries in the breadcrumbs 
registry.

Links
*****

* Download his `PyPi package <http://pypi.python.org/pypi/autobreadcrumbs>`_;
* Clone it on his `Github repository <https://github.com/sveetch/autobreadcrumbs>`_;
* Documentation and demo to come on his `DjangoSveetchies page <http://sveetchies.sveetch.net/autobreadcrumbs/>`_.

Install
=======

In your *settings* file add **AutoBreadcrumbs** to your installed apps :

::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        ...
    )

Then register his *context processor* :

::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )

And finally, as for the *autodiscover* for the admin site (``django.contrib.admin``), you will have to add these 
two lines in your ``urls.py`` project :

::

    import autobreadcrumbs
    autobreadcrumbs.autodiscover()

This is optionnally but if you don't do this, all ``crumbs.py`` file will be ignored.

Usage
=====

Note that this app will don't work correctly if you don't have a strong organisation in your 
urls map.

* You must ensure that all your urls are correctly named (see 
  `Naming URL patterns <https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns>`_);
* Different views must not use the same url;
* Regroup your restricted views on some url paths and don't mix them with non-restricted view urls.

View registration
*****************

Registration
------------

The *context processor* makes a search from the current url that is splitted in segments which represent 
the crumbs. For each segment, an entry is searched on his URL name in the breadcrumbs registry in this 
step order :

#. If the name has an entry in ``settings.AUTOBREADCRUMBS_TITLES``, then use it;
#. If the name has an entry in a ``crumbs.py`` file in one of your apps, then use it;
#. If the view has an attribute ``crumb_titles``, then try to find the URL name to use it, otherwise continue; 
#. If the view has an attribute ``crumb_title``, then use it;

If none of these steps succeeds to find the URL name, the ressource will be ignored and not be displayed 
in the breadcrumbs.

If you need to *hide* a ressource from breadcrumbs, just set his URL name to a *None* value, this will act in 
ignoring the ressource.

A crumb title value use the Django template system to be rendered and is aware of the context of the template 
where it is called, so you can use all available template filters, tags and variables in your crumb titles.

.. NOTE:: ``crumb_titles`` and ``crumb_title`` will be deprecated in the next release as the decorators for *view 
          functions*.

App crumbs
~~~~~~~~~~

Applications should define their crumbs in a ``crumbs.py`` file like this :

::

    from autobreadcrumbs import site
    from django.utils.translation import ugettext_lazy
    
    site.update({
        ...
        'documents-index': ugettext_lazy('Sitemap'),
        ...
    })

Note the usage of ``ugettext_lazy`` to get translated strings, if you don't use the `Django internationalization system`_ in your 
project you can avoid it, but if you plan to use it you must apply ``ugettext_lazy`` on your title strings.

Project crumbs
~~~~~~~~~~~~~~

Also you can register crumbs in your project settings :

::

    AUTOBREADCRUMBS_TITLES = {
        "pages-index1": u"My index",
        "pages-index2": u"My index alternative",
    }

Crumbs setted in project settings have the higher priority on application crumbs. As for `App crumbs`_ you should use 
``ugettext_lazy`` on your title strings.

Template context
****************

In all your templates laying that have the global context, two additional variables (`autobreadcrumbs_elements`_ and 
`autobreadcrumbs_current`_) will be added by the *context processor*.

autobreadcrumbs_elements
------------------------

This variable will contain the breadcrumb as a list of crumbs in the correct order, where each crumb will be 
a ``BreadcrumbRessource`` instance. A ``BreadcrumbRessource`` instance contains the following attributes :

* ``path`` : relative path to the ressource URL;
* ``name`` : the ressource name (that is the name of the URL linked to the ressource);
* ``title`` : the ressource title to be displayed;
* ``view_args`` : argument list given to the ressource view;
* ``view_kwargs`` : named argument list given to the ressource view;

autobreadcrumbs_current
-----------------------

This variable will contains the ``BreadcrumbRessource`` instance of the current crumb, this instance is the same as 
the last list item in the `autobreadcrumbs_elements`_.

Template tags
*************

These tags are avalaible after loading their library in your templates : ::

    {% load autobreadcrumb %}

current_title_from_breadcrumbs
  This simply returns the title from the current ressource.
autobreadcrumbs_tag
  Builds the breadcrumb HTML using the ``autobreadcrumbs_tag.html`` template.
autobreadcrumbs_links
  Builds the breadcrumb HTML using the template strings in ``settings.AUTOBREADCRUMBS_HTML_LINK`` and 
  ``settings.AUTOBREADCRUMBS_HTML_SEPARATOR``.
currentwalkthroughto
  Returns the content tag if the current ressource walk through the given ressource URL name.
  
  Example : ::
  
      {% currentwalkthroughto 'index' %}This pas walk through the named url 'index'{% endcurrentwalkthroughto %}
  
  If the test fail, the tag return an empty string.

