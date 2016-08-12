import pytest

from autobreadcrumbs.discover import discover, autodiscover


#def setup_function(function):
    #"""Reset registry for every test function from this file"""
    #breadcrumbs_registry.reset()


@pytest.mark.parametrize("module_path,filename,loaded_path", [
    ('project', 'urls', 'project.urls'),
    ('project.foo', 'crumbs', 'project.foo.crumbs'),
])
def test_discover_success(module_path, filename, loaded_path):
    """Simple discovering"""
    assert discover(module_path, filename) == loaded_path


@pytest.mark.parametrize("module_path,filename", [
    ('project', 'nope'),
    ('project.foo', 'nope'),
])
def test_discover_missing(module_path, filename):
    """Try discovering on non-existing filename"""
    assert discover(module_path, filename) == None


@pytest.mark.parametrize("module_path,filename", [
    ('project.foo', 'failure'),
])
def test_discover_error(module_path, filename):
    """Attempt exception raised from file with errors"""
    with pytest.raises(SyntaxError):
        discover(module_path, filename)


@pytest.mark.parametrize("module_path,filename", [
    ('project.foo', 'failure'),
])
def test_autodiscover(module_path, filename):
    """Attempt exception raised from file with errors"""
    names = autodiscover()

    assert names == ['project.foo.crumbs']
