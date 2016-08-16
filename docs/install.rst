
=======
Install
=======

::

    pip install autobreadcrumbs


Then register the app in your project settings like this :

.. sourcecode:: python

    INSTALLED_APPS = (
        ...
        'rstview',
        ...
    )

Also you can overrides some default settings from your project settings file.

Once done, your project can use rstview template tags and views.

In your *settings* file add **AutoBreadcrumbs** to your installed apps :

.. sourcecode:: python

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        ...
    )

Import default settings:

.. sourcecode:: python

    from autobreadcrumbs.settings import *

Then register its *context processor* :

.. sourcecode:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )

Finally, you will have to add these two lines in your ``urls.py`` project :

.. sourcecode:: python

    import autobreadcrumbs
    autobreadcrumbs.autodiscover()

This is optional but if you don't do this, all ``crumbs.py`` file will be
ignored and only titles defined in ``settings.AUTOBREADCRUMBS_TITLES`` will be used.
