# -*- coding: utf-8 -*-
"""
Crumb definitions discovering
=============================

Crumb definitions are registred through files that are loaded as Python
modules, where some code can register needed crumbs.
"""
import copy
from django.conf import settings
from importlib import import_module
from django.utils.module_loading import module_has_submodule

from autobreadcrumbs.registry import breadcrumbs_registry


def discover(module_path, filename=None):
    """
    Try to discover and load a ``crumbs.py`` file from given Python path.

    Arguments:
        module_path (string): Python path to scan for ``filename`` module.

    Keyword Arguments:
        filename (string): Optional module filename to search for, usually
            ``crumbs.py``, default to ``None``.

    Raises:
        Exception: Raise any occuring exception from loaded Python path.

    Returns:
        string or None: Python path (``module.filename``) for discovered
        crumbs module. If ``filename`` does not exists in module,
        return ``None``.
    """
    mod = import_module(module_path)
    name = module_path
    if filename:
        name = '{path}.{filename}'.format(path=module_path, filename=filename)

    # Attempt to import the app's admin module.
    try:
        # Keep registry safe in case of error
        before_import_registry = copy.copy(breadcrumbs_registry._registry)
        # Import crumbs module
        import_module(name)
    except:
        # Reset the model registry to the state before exception occured
        breadcrumbs_registry._registry = before_import_registry

        # Only bubble up error if app have a crumbs file, dont raise anything
        # if it lacks of if (unobtrusive way)
        if module_has_submodule(mod, filename):
            raise
        else:
            return None
    else:
        return name


def autodiscover(filename='crumbs'):
    """
    Automatic discovering for available crumbs definitions

    Before looking at crumbs files, registry start from
    ``settings.AUTOBREADCRUMBS_TITLES`` items if setted, else an empty Dict.

    Then it try to load possible root crumb file defined in
    ``settings.AUTOBREADCRUMBS_ROOT_CRUMB`` (as a Python path). And finally
    load each crumbs file finded in ``settings.INSTALLED_APPS``.

    Keyword Arguments:
        filename (string): Module filename to search for. Default to
            ``crumbs``, so it will search for a ``crumbs.py`` file at root of
            every enabled module from ``settings.INSTALLED_APPS``.

    Returns:
        list: List of successfully loaded Python paths.
    """
    paths = []

    # Directly fill registry from initial crumbs setting
    breadcrumbs_registry.update(getattr(settings, 'AUTOBREADCRUMBS_TITLES',
                                        {}))

    # Fill paths to discover from project level crumb file
    root_crumbs = getattr(settings, 'AUTOBREADCRUMBS_ROOT_CRUMB', None)
    if root_crumbs:
        paths.append(discover(root_crumbs))

    # Fill paths to discover from installed apps
    apps = list(settings.INSTALLED_APPS)

    paths = paths + [discover(app, filename=filename) for app in apps]

    return filter(None, paths)
