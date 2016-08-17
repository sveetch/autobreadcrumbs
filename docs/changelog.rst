
=========
Changelog
=========

Version 2.0.0 - 2016/08/18
--------------------------

This is a major refactoring to adopt Test Driven Development, cleaner behaviors and better core API.

* Added Unittests with Py.test;
* Added tox configuration;
* Added documentation;
* Moved discovering from ``context_processors.py`` to ``discover.py``;
* Moved regitry stuff from ``__init__.py`` to ``registry.py``;
* Better docstring for code;
* Many minor changes to follow Flake8;
* Added ``AUTOBREADCRUMBS_ROOT_CRUMB`` setting to be able to use a ``crumbs.py`` module at project root;
* Dropped support for Django < 1.6;
* Added support for Django 1.9;

Version 1.1.0 - 2015/08/18
--------------------------

* Do not use django.utils.importlib anymore since it's deprecated in Django>=1.7, instead use Python2.7 importlib module;
* Added relevant meta datas for package;

Version 1.0.0 - 2014/08/12
--------------------------

* Added url namespace support;
* Changed setup.py to add requirement for Django>=1.5;
* Fixed issue with root url that was ignored in the crumbs;
* Dropped support for Django < 1.5;

Version 0.9.0 - 2014/01/26
--------------------------

* Changed tuple form for crumb entry;
* Updated README;
* Fixed compatibilty with Django >= 1.5;
* Fixed error too many values;
* Fixed ``setup.py``;
* Fixed MANIFEST;
