Plugins
=======

Plugin support was added in v2.0.

Writing plugins
---------------

PyPOM uses `pluggy`_ to enable support for plugins. In order to write a plugin
you can create an installable Python package with a specific entry point. For
example, the following (incomplete) ``setup.py`` will register a plugin named
screenshot::

  from setuptools import setup

  setup(name='PyPOM-screenshot',
        description='plugin for PyPOM that takes a lot of screenshots',
        packages=['pypom_screenshot'],
        install_requires=['PyPOM'],
        entry_points={'pypom.plugin': ['screenshot = pypom_screenshot.plugin']})

Then, in your package implement one or more of the plugin :ref:`hooks` provided
by PyPOM. The following example will take a screenshot whenever a page or
region has finished loading::

  def pypom_after_wait_for_page_to_load(page):
      page.selenium.get_screenshot_as_file(page.__class__.__name__ + '.png')


  def pypom_after_wait_for_region_to_load(region):
      region.root.screenshot(region.__class__.__name__ + '.png')

.. _pluggy: https://pluggy.readthedocs.io/
