Release Notes
=============

**2.0.0 (unreleased)**

* Added support for plugins.

  * This introduces plugin hooks ``pypom_after_wait_for_page_to_load`` and
    ``pypom_after_wait_for_region_to_load``.
  * In order to take advantage of plugin support you must avoid implementing
    ``wait_for_page_to_load`` or ``wait_for_region_to_load`` in your page
    objects.
  * This was previously the only way to implement a custom wait for your pages
    and regions, but now means the calls to plugin hooks would be bypassed.
  * Custom waits can now be achieved by implementing a ``loaded`` property on
    the page or region, which returns ``True`` when the page or region has
    finished loading.
  * See the user guide for more details.

* Any unused ``url_kwargs`` after formatting ``URL_TEMPLATE`` are added as URL
  query string parameters.

**1.3.0 (2018-02-28)**

* Added support for EventFiringWebDriver

  * Thanks to `@Greums <https://github.com/Greums>`_ for the PR

**1.2.0 (2017-06-20)**

* Dropped support for Python 2.6

**1.1.1 (2016-11-21)**

* Fixed packaging of ``pypom.interfaces``

**1.1.0 (2016-11-17)**

* Added support for Splinter

  * Thanks to `@davidemoro <https://github.com/davidemoro>`_ for the PR

**1.0.0 (2016-05-24)**

* Official release
