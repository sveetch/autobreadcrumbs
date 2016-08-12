# -*- coding: utf-8 -*-
"""
Site registry for breadcrumb titles
===================================

"""
class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class BreadcrumbSite(object):
    """
    Breadcrumbs registry
    """
    def __init__(self, *args, **kwargs):
        # title_key (string) -> title_name (string)
        self._registry = kwargs.get('initial', {})

    def reset(self):
        """
        Reset registry to an empty Dict
        """
        self._registry = {}

    def get_registry(self):
        return self._registry

    def get_names(self):
        return sorted(self._registry.keys())

    def has_title(self, key):
        return key in self._registry

    def get_title(self, key):
        """
        Get the internationalized title if i18n is used

        :type key: string
        :param key: title key

        :rtype: string
        :return: the translated title
        """
        if not self.has_title(key):
            raise NotRegistered('The title key "{}" is not registered'.format(key))
        return self._registry[key]

    def register(self, key, value):
        """
        Register a title key

        Raise ``AlreadyRegistered`` if the key is allready registered

        :type key: string
        :param key: the title key to add

        :type value: string
        :param value: title value
        """
        if self.has_title(key):
            raise AlreadyRegistered('The title key "{}" is already registered'.format(key))
        # Instantiate the admin class to save in the registry
        self._registry[key] = value

    def unregister(self, key):
        """
        Unregister a title key

        Raise ``NotRegistered`` if the key is not registered

        :type key: string
        :param key: the title key to remove
        """
        if not self.has_title(key):
            raise NotRegistered('The title key "{}" is not registered'.format(key))
        del self._registry[key]

    def update(self, crumbs):
        """
        Update registry with many titles

        :type crumbs: dict
        :param key: Titles dict (key -> name)
        """
        self._registry.update(crumbs)


# Default breadcrumbs site
breadcrumbs_registry = BreadcrumbSite()
