==============
django-popular
==============

A simple interface to use Google Analytics data to determine things like
most popular blog posts.  By associating a model with a `Google Analytics
compatible regex_` and an optional lookup function, it is possible to
find the most popular instances of the registered model.

The current requirement to write an additional regex and function is
acknowledged as sub-optimal, alternatives are welcome, though the limitations
of the Google Analytics API make reusing the regex from the urlconf impossible.

.. _http://www.google.com/support/analytics/bin/answer.py?answer=55582

Installation
============

You can obtain the latest release of django-popular via
`PyPI <http://pypi.python.org/pypi/django-popular>`_ or check out the
`latest source <http://github.com/sunlightlabs/django-popular>`_

To install a source distribution::

    python setup.py install

It is also possible to install django-popular with
`pip <http://pypi.python.org/pypi/pip>`_ or easy_install.

In order to use the template tag, ``'popular'`` must be added to your
``INSTALLED_APPS``.

Usage
=====

To be written once the API has stabilized, for now look at ``__init__.py``
and ``templatetags/popular.py``.

Todo
====

    * explore non-google analytics options
    * reduce complexity in registering a new model
