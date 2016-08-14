import pytest
"""
WARNING: There is an issue with the way Autobreadcrumbs registry is feeded.

Imports are somewhat "cached" and so if we try to reset the registry between
tests, crumbs modules won't feed them again during discovering, even trying
to import them manually (without importlib).

Tampering ``sys.modules`` would seem a solution:

    http://stackoverflow.com/questions/2918898/prevent-python-from-caching-the-imported-modules
"""


def test_autodiscover():
    """Check registred crumb names after autodiscover"""
    from autobreadcrumbs.registry import breadcrumbs_registry

    # Autodiscovering is disabled since it allready have be executed
    # previously, see previous warning
    #from autobreadcrumbs.discover import autodiscover
    #print autodiscover()

    assert breadcrumbs_registry.get_names() == [
        'bar',
        'bar-ometer',
        'foo:controlled-false',
        'foo:controlled-false-endpoint',
        'foo:controlled-true',
        'foo:controlled-true-endpoint',
        'foo:date',
        'foo:index',
        'foo:invisible-chu',
        'foo:pika',
        'foo:pika-chu',
        'foo:slug',
        'foo:subfoo:index',
        'foo:subfoo:plop',
        'home',
    ]
