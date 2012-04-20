.. _breadcrumb: http://en.wikipedia.org/wiki/Breadcrumb_%28navigation%29#Websites

Introduction
============

**AutoBreadcrumbs** is a Django application to automatically build a breadcrumb in your website like 
this : ::

  Home > Some page > Some child page

Each *crumb* displays a title with a link to represent a view, the crumb tree is determined from the urls map 
of your project, their titles and links are determined from the associated view entries, either given in the 
settings or directly added as view attributes (only with view functions).

You can download it on his `Github repository <https://github.com/sveetch/autobreadcrumbs>`_ and find his 
`documentation on DjangoSveetchies <http://sveetchies.sveetch.net/autobreadcrumbs/>`_.

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

The *context processor* makes a search from the current url that will be splitted in segments which will 
generate the crumbs.

To be registred as a crumb, your view must have a static attribute ``crumb_title`` (*string*) or 
``crumb_titles`` (*dict*), or an entry in ``settings.AUTOBREADCRUMBS_TITLES`` as a tuple 
``(url-name, title)``.

Attribute ``crumb_titles`` is used to register different URLs on a same view, attribute ``crumb_title`` 
attends to simply register a view to an unique URL. They are both used only with *view functions*.

The context processor makes his search using the view object and the associated URL name in this step
order :

#. If the name has an entry in ``settings.AUTOBREADCRUMBS_TITLES``, then use it;
#. If the view has an attribute ``crumb_titles``, then try to find the URL name to use it, otherwise continue; 
#. If the view has an attribute ``crumb_title``, then use it;

If none of these steps succeeds to find the URL name, the ressource will be ignored and not be displayed 
in the breadcrumb.

.. NOTE:: *Class based views* since Django 1.3.x are registrable only in 
          ``settings.AUTOBREADCRUMBS_TITLES``.

Exclude
-------

The decorator ``@autobreadcrumb_hide`` can be used on view functions to ignore them in breacrumbs,  
you can also simply define a ``None`` value in titles, this will act in ignoring the ressource.

Examples
--------

Simple example with a view function :

::

    @autobreadcrumb_add(u"My index")
    def index(request):
        ....

For different URLs with different titles on the same view :

::

    @autobreadcrumb_add({
        "pages-index1": u"My first index",
        "pages-index2": u"My second index",
    })
    def index(request):
        ....

.. autobreadcrumbs_titles

In your settings :

::

    AUTOBREADCRUMBS_TITLES = {
        "pages-index1": u"Mon zuper zindex",
        "pages-index2": u"My upper index",
    }

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

These tags are avalaible after loading their library in your templates :

::

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

