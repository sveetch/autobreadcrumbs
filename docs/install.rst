
=======
Install
=======

::

    pip install autobreadcrumbs


#. In your *settings* file add **autobreadcrumbs** to your installed apps:

    .. sourcecode:: python

        INSTALLED_APPS = (
            ...
            'autobreadcrumbs',
            ...
        )

#. Import default settings:

    .. sourcecode:: python

        from autobreadcrumbs.settings import *

#. Register its *context processor*:

    .. sourcecode:: python

        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
            ...
        )

    (Order with other context processors don't matter).

#. Finally add these two lines in your main ``urls.py``:

    .. sourcecode:: python

        import autobreadcrumbs
        autobreadcrumbs.autodiscover()

    This is optional but if you don't do this, all ``crumbs.py`` file will be
    ignored and only titles defined in ``settings.AUTOBREADCRUMBS_TITLES`` will be used.
