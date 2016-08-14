import pytest

from autobreadcrumbs.registry import AlreadyRegistered, NotRegistered, BreadcrumbSite


def test_registry_empty():
    """Initial empty registry"""
    registry = BreadcrumbSite()

    assert registry.get_registry() == {}


def test_registry_initial():
    """Registry initially filled"""
    registry = BreadcrumbSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.get_registry() == {
        'foo': 42,
        'bar': True,
    }


def test_check_breadcrumb_reset():
    """Reseting registry"""
    registry = BreadcrumbSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })
    registry.reset()

    assert registry.get_registry() == {}


def test_check_breadcrumb_names():
    """Get registred names"""
    registry = BreadcrumbSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.get_names() == [
        'bar',
        'foo',
    ]


@pytest.mark.parametrize("name,exists", [
    ('foo', True),
    ('bar', True),
    ('nope', False),
    ('Foo', False),
])
def test_check_breadcrumb_hastitle(name, exists):
    """Check if a title exist in registry"""
    registry = BreadcrumbSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.has_title(name) == exists


def test_check_breadcrumb_gettitle():
    """Check if a title exist in registry"""
    registry = BreadcrumbSite()
    registry.update({
        'foo': 42,
        'bar': True,
    })

    assert registry.get_title('foo') == 42

    with pytest.raises(NotRegistered):
        registry.get_title('nope')


def test_check_breadcrumb_register():
    """Register title"""
    registry = BreadcrumbSite()

    registry.register('foo', True)
    registry.register('bar', 42)

    assert registry.get_names() == [
        'bar',
        'foo',
    ]

    with pytest.raises(AlreadyRegistered):
        registry.register('foo', True)


def test_check_breadcrumb_unregister():
    """Unregister title"""
    registry = BreadcrumbSite()

    registry.register('foo', True)
    registry.register('bar', 42)

    assert registry.get_names() == [
        'bar',
        'foo',
    ]

    registry.unregister('foo')
    assert registry.get_names() == [
        'bar',
    ]

    with pytest.raises(NotRegistered):
        registry.unregister('plip')
