# -*- coding: utf-8 -*-
"""
Site registry for breadcrumb definitions
========================================

"""


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class BreadcrumbSite(object):
    """
    Breadcrumbs site registry

    Keyword Arguments:
        initial (dict): Optional initial dictionnary of crumbs
            ``urlname->value``. Default to an empty dict.
    """
    def __init__(self, *args, **kwargs):
        self._registry = kwargs.get('initial', {})

    def reset(self):
        """
        Reset registry to an empty Dict.
        """
        self._registry = {}

    def get_registry(self):
        """
        Return current registry

        Returns:
            dict: Currrent registry.
        """
        return self._registry

    def get_names(self):
        """
        Return registred crumb url names.

        Returns:
            list: List of registred crumb url names, sorted with default
            ``sorted()`` behavior.
        """
        return sorted(self._registry.keys())

    def has_title(self, name):
        """
        Find if given name is registred as a crumb.

        Returns:
            bool: ``True`` if name exists in current registry, else ``False``.
        """
        return name in self._registry

    def get_title(self, name):
        """
        Get title for given url name.

        Arguments:
            name (string): Url name.

        Returns:
            string or tuple: Crumb title.
        """
        if not self.has_title(name):
            raise NotRegistered(('The url name "{}" is not registered as a '
                                 'crumb.').format(name))
        return self._registry[name]

    def register(self, name, value):
        """
        Register a crumb for given url name.

        Arguments:
            name (string): Url name.
            value (string or tuple): Crumb title to define.

        Raises:
            ``AlreadyRegistered`` if the url name is allready registered in
            crumbs.
        """
        if self.has_title(name):
            raise AlreadyRegistered(('The url name "{}" is already registered '
                                     'as a crumb.').format(name))
        # Instantiate the admin class to save in the registry
        self._registry[name] = value

    def unregister(self, name):
        """
        Unregister a crumb.

        Arguments:
            name (string): Url name.

        Raises:
            ``NotRegistered`` if given url name is not registred yet.
        """
        if not self.has_title(name):
            raise NotRegistered(('The url name "{}" is not registered yet as '
                                 'a crumb.').format(name))
        del self._registry[name]

    def update(self, crumbs):
        """
        Update many crumbs

        This works like the ``Dict.update({..})`` method.

        Arguments:
            crumbs (dict): A dict of crumbs (``urlname->value``).
        """
        self._registry.update(crumbs)


#: Default breadcrumbs site registry for a Django instance.
breadcrumbs_registry = BreadcrumbSite()
