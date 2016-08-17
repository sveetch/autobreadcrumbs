
========
Overview
========

Autobreadcrumbs build breadcrumbs for a view using its url to find other views the url goes through.

Crumb principle is to link a crumb title to an url name. You can't add a crumb that is not related to an url name.

There are three way to define crumbs:

* In the initial crumb dictionnary ``settings.AUTOBREADCRUMBS_TITLES``;
* At project level in a crumb module that will be loaded from defined Python path in ``settings.AUTOBREADCRUMBS_ROOT_CRUMB``;
* Per application with a crumb module in your application enabled from ``settings.INSTALLED_APPS``;

The first way is a simple dictionnary to populate. The other ways use Python modules that will directly manage crumbs using the registry interface.

When crumbs are defined, they need to be discovered so they can be loaded to populate registry.

Finally the template context processor is in charge to resolve breadcrumbs for current ressource (a view instance) and push resolved datas in template context.

Example
*******

With following main ``urls.py``:

.. sourcecode:: python

    from django.conf.urls import include, url
    from django.views.generic.base import TemplateView

    urlpatterns = [
        url(r'^$', TemplateView.as_view(
            template_name="page.html"
        ), name='home'),

        url(r'^foo/$', TemplateView.as_view(
            template_name="page.html"
        ), name='foo'),

        url(r'^foo/bar/$', TemplateView.as_view(
            template_name="page.html"
        ), name='bar'),
    ]

Following settings:

.. sourcecode:: python

    AUTOBREADCRUMBS_TITLES = {
        'home': 'Home',
    }
    # Assume your django project is a 'project/' directory
    AUTOBREADCRUMBS_ROOT_CRUMB = 'project.crumbs'

And following ``crumbs.py`` at project root:

.. sourcecode:: python

    from autobreadcrumbs.registry import breadcrumbs_registry
    from django.utils.translation import ugettext_lazy

    breadcrumbs_registry.update({
        'foo': 'Foo',
        'bar': ugettext_lazy("Bar"),
    })

The view at ``/foo/bar/`` will resolve current ressource is passing through url names *home*, *foo* and finally *bar*.

This will lead to breadcrumbs: ::

    Home > Foo > Bar

You can see usage of ``ugettext_lazy`` that can be used to store translation string for your titles if needed.
