User Guide
==========

.. contents:: :depth: 3

Upgrading to 2.0
----------------

Plugin support was introduced in v2.0, and if you're upgrading from an earlier
version you may need to make some changes to take advantage of any plugins.
Before this version, to implement a custom wait for pages/regions to finish
loading it was necessary to implement ``wait_for_page_to_load`` or
``wait_for_region_to_load``. If you haven't implemented either of these, you
don't need to do anything to upgrade. If you have, then whilst your custom
waits will still work, we now support plugins that can be triggered after a
page/region load, and these calls are made from the base classes. By overriding
the default behaviour, you may be missing out on triggering any plugin
behaviours. Rather than having to remember to always call the same method from
the parent, you can simply change your custom wait to a new ``loaded`` property
that returns ``True`` when the page/region has loaded.

So, if you have implemented your own
:py:func:`~pypom.page.Page.wait_for_page_to_load` like this::

  def wait_for_page_to_load(self):
      self.wait.until(lambda s: self.seed_url in s.current_url)

You will want to change it to use :py:attr:`~pypom.page.Page.loaded` like this::

  @property
  def loaded(self):
      return self.seed_url in self.selenium.current_url

Similarly, if you have implemented your own
:py:func:`~pypom.region.Region.wait_for_region_to_load` like this::

  def wait_for_region_to_load(self):
      self.wait.until(lambda s: self.root.is_displayed())

You will want to change it to use :py:attr:`~pypom.region.Region.loaded` like
this::

  @property
  def loaded(self):
      return self.root.is_displayed()

Drivers
-------

PyPOM requires a driver object to be instantiated, and supports multiple driver
types. The examples in this guide will assume that you have a driver instance.

Selenium
~~~~~~~~

To instantiate a Selenium_ driver you will need a
:py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object::

  from selenium.webdriver import Firefox
  driver = Firefox()

Splinter
~~~~~~~~

To instantiate a Splinter_ driver you will need a :py:class:`~splinter.Browser`
object::

  from splinter import Browser
  driver = Browser()

Pages
-----

Page objects are representations of web pages. They provide functions to allow
simulating user actions, and providing properties that return state from the
page. The :py:class:`~pypom.page.Page` class provided by PyPOM provides a
simple implementation that can be sub-classed to apply to your project.

The following very simple example instantiates a page object representing the
landing page of the Mozilla website::

  from pypom import Page

  class Mozilla(Page):
      pass

  page = Mozilla(driver)

If a page has a seed URL then you can call the :py:func:`~pypom.page.Page.open`
function to open the page in the browser. There are a number of ways to specify
a seed URL.

Base URL
~~~~~~~~

A base URL can be passed to a page object on instantiation. If no URL template
is provided, then calling :py:func:`~pypom.page.Page.open` will open this base
URL::

  from pypom import Page

  class Mozilla(Page):
      pass

  base_url = 'https://www.mozilla.org'
  page = Mozilla(driver, base_url).open()

URL templates
~~~~~~~~~~~~~

By setting a value for :py:attr:`~pypom.page.Page.URL_TEMPLATE`, pages can
specify either an absolute URL or one that is relative to the base URL (when
provided). In the following example, the URL https://www.mozilla.org/about/
will be opened::

  from pypom import Page

  class Mozilla(Page):
      URL_TEMPLATE = '/about/'

  base_url = 'https://www.mozilla.org'
  page = Mozilla(driver, base_url).open()

As this is a template, any additional keyword arguments passed when
instantiating the page object will attempt to resolve any placeholders. In the
following example, the URL https://www.mozilla.org/de/about/ will be opened::

  from pypom import Page

  class Mozilla(Page):
      URL_TEMPLATE = '/{locale}/about/'

  base_url = 'https://www.mozilla.org'
  page = Mozilla(driver, base_url, locale='de').open()

URL parameters
~~~~~~~~~~~~~~

Any keyword arguments provided that are not used as placeholders in the URL
template are added as query string parameters. In the following example, the
URL https://developer.mozilla.org/fr/search?q=bold&topic=css will be opened::

  from pypom import Page

  class Search(Page):
      URL_TEMPLATE = '/{locale}/search'

  base_url = 'https://developer.mozilla.org/'
  page = Search(driver, base_url, locale='fr', q='bold', topic='css').open()

Waiting for pages to load
~~~~~~~~~~~~~~~~~~~~~~~~~

Whenever a driver detects that a page is loading, it does its best to block
until it's complete. Unfortunately, as the driver does not know your
application, it's quite common for it to return earlier than a user would
consider the page to be ready. For this reason, the
:py:attr:`~pypom.page.Page.loaded` property can be overridden and customised
for your project's needs by returning ``True`` when the page has loaded. This
property is polled by :py:func:`~pypom.page.Page.wait_for_page_to_load`, which
is called by :py:func:`~pypom.page.Page.open` after loading the seed URL, and
can be called directly by functions that cause a page to load.

The following example waits for the seed URL to be in the current URL. You can
use this so long as the URL is not rewritten or redirected by your
application::

  from pypom import Page

  class Mozilla(Page):

      @property
      def loaded(self):
          return self.seed_url in self.selenium.current_url

Other things to wait for might include when elements are displayed or enabled,
or when an element has a particular class. This will be very dependent on your
application.

Regions
-------

Region objects represent one or more elements of a web page that are repeated
multiple times on a page, or shared between multiple web pages. They prevent
duplication, and can improve the readability and maintainability of your page
objects.

Root elements
~~~~~~~~~~~~~

It's important for page regions to have a root element. This is the element
that any child elements will be located within. This means that page region
locators do not need to be unique on the page, only unique within the context
of the root element.

If your page region contains a :py:attr:`~pypom.region.Region._root_locator`
attribute, this will be used to locate the root element every time an instance
of the region is created. This is recommended for most page regions as it
avoids issues when the root element becomes stale.

Alternatively, you can locate the root element yourself and pass it to the
region on construction. This is useful when creating regions that are repeated
on a single page.

The root element can later be accessed via the
:py:attr:`~pypom.region.Region.root` attribute on the region, which may be
necessary if you need to interact with it.

Repeating regions
~~~~~~~~~~~~~~~~~

Page regions are useful when you have multiple items on a page that share the
same characteristics, such as a list of search results. By creating a page
region, you can interact with any of these items in a common way:

The following example uses Selenium_ to locate all results on a page and return
a list of ``Result`` regions. This can be used to determine the number of
results, and each result can be accessed from this list for further state or
interactions. Refer to `locating elements`_ for more information on how to
write locators for your driver:

.. literalinclude:: examples/repeated_regions.html
   :language: html
   :emphasize-lines: 6-23

.. literalinclude:: examples/repeated_regions.py
   :language: python
   :emphasize-lines: 6-8
   :lines: 5-24

Nested regions
~~~~~~~~~~~~~~

Regions can be nested inside other regions (i.e. a menu region with multiple entry
regions). In the following example a main page contains two menu regions that
include multiple repeated entry regions:

.. literalinclude:: examples/nested_regions.html
   :language: html

As a region requires a page object to be passed you need
to pass ``self.page`` when instantiating nested regions:

.. literalinclude:: examples/nested_regions.py
   :language: python
   :emphasize-lines: 4-5,9-10,16-18
   :lines: 5-30


Shared regions
~~~~~~~~~~~~~~

Pages with common characteristics can use regions to avoid duplication.
Examples of this include page headers, navigation menus, login forms, and
footers. These regions can either be defined in a base page object that is
inherited by the pages that contain the region, or they can exist in their own
module:

In the following example, any page objects that extend ``Base`` will inherit
the ``header`` property, and be able to check if it's displayed. Refer to
`locating elements`_ for more information on how to write locators for your
driver::

  from pypom import Page, Region
  from selenium.webdriver.common.by import By

  class Base(Page):

      @property
      def header(self):
          return self.Header(self)

      class Header(Region):
          _root_locator = (By.ID, 'header')

          def is_displayed(self):
              return self.root.is_displayed()

Waiting for regions to load
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :py:attr:`~pypom.region.Region.loaded` property function can be
overridden and customised for your project's needs by returning ``True`` when
the region has loaded to ensure it's ready for interaction. This property is
polled by :py:attr:`~pypom.region.Region.wait_for_region_to_load`, which is
called whenever a region is instantiated, and can be called directly by
functions that a region to reload.

The following example waits for an element within a page region to be
displayed::

  from pypom import Region

  class Header(Region):

      @property
      def loaded(self):
          return self.root.is_displayed()

Other things to wait for might include when elements are displayed or enabled,
or when an element has a particular class. This will be very dependent on your
application.

Locating elements
-----------------

Each driver has its own approach to locating elements. A suggested approach is
to store your locators at the top of your page/region classes. Ideally these
should be preceeded with a single underscore to indicate that they're primarily
reserved for internal use. These attributes can be stored as a two item tuple
containing both the strategy and locator, and can then be unpacked when passed
to a method that requires the arguments to be separated.

Selenium
~~~~~~~~

The :py:class:`~selenium.webdriver.common.by.By` class covers the common
locator strategies for Selenium_. The following example shows a locator being
defined and used in a page object::

  from pypom import Page
  from selenium.webdriver.common.by import By

  class Mozilla(Page):
      _logo_locator = (By.ID, 'logo')

      @property
      def loaded(self):
          logo = self.find_element(*self._logo_locator)
          return logo.is_displayed()

Splinter
~~~~~~~~

The available locator strategies for Splinter_ are:

* name
* id
* css
* xpath
* text
* value
* tag

The following example shows a locator being defined and used in a page object::

    from pypom import Page
    from selenium.webdriver.common.by import By

    class Mozilla(Page):
        _logo_locator = ('id', 'logo')

        @property
        def loaded(self):
            logo = self.find_element(*self._logo_locator)
            return logo.is_displayed()

Explicit waits
--------------

For convenience, a :py:class:`~selenium.webdriver.support.wait.WebDriverWait`
object is instantiated with an optional timeout (with a default of 10 seconds)
for every page. This allows your page objects to define an explicit wait
whenever an interaction causes a reponse that a real user would wait for before
continuing. For example, checking a box might make a button become enabled. If
we didn't wait for the button to become enabled we may try clicking on it too
early, and nothing would happen. Another example of where explicit waits are
common is when `waiting for pages to load`_ or `waiting for regions to load`_.

The following example uses Selenium_ to demonstrate a wait that is necessary
after checking a box that causes a button to become enabled. Refer to
`locating elements`_ for more information on how to write locators for your
driver::

  from pypom import Page
  from selenium.webdriver.common.by import By

  class Mozilla(Page):
      _privacy_policy_locator = (By.ID, 'privacy')
      _sign_me_up_locator = (By.ID, 'sign_up')

      def accept_privacy_policy(self):
          self.find_element(*self._privacy_policy_locator).click()
          sign_me_up = self.find_element(*self._sign_me_up_locator)
          self.wait.until(lambda s: sign_me_up.is_enabled())

You can either specify a timeout by passing the optional ``timeout`` keyword
argument when instantiating a page object, or you can override the
:py:func:`~pypom.page.Page.__init__` method if you want your timeout to be
inherited by a base project page class.

.. note::

  The default timeout of 10 seconds may be considered excessive, and you may
  wish to reduce it. It it not recommended to increase the timeout however. If
  you have interactions that take longer than the default you may find that you
  have a performance issue that will considerably affect the user experience.

.. _Selenium: http://docs.seleniumhq.org/
.. _Splinter: https://github.com/cobrateam/splinter
