User Guide
==========

.. contents:: :depth: 3

Pages
-----

Page objects are representations of web pages. They provide functions to allow
simulating user actions, and providing properties that return state from the
page. The :py:class:`~pypom.page,Page` class provided by PyPOM provides a
simple implementation that can be sub-classed to apply to your project.

To instantiate a page object with PyPOM you will need a Selenium_
:py:class:`~selenium.webdriver.remote.webdriver.WebDriver` object. The
following very simple example opens the Mozilla website in Firefox, and
instantiates a page object representing the landing page::

  from pypom import Page
  from selenium.webdriver import Firefox

  class Mozilla(Page):
      pass

  driver = Firefox()
  driver.get('https://www.mozilla.org')
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
  from selenium.webdriver import Firefox

  class Mozilla(Page):
      pass

  base_url = 'https://www.mozilla.org'
  driver = Firefox()
  page = Mozilla(driver, base_url).open()

URL templates
~~~~~~~~~~~~~

By setting a value for :py:attr:`~pypom.page.Page.URL_TEMPLATE`, pages can
specify either an absolute URL or one that is relative to the base URL (when
provided). In the following example the URL https://www.mozilla.org/about/ will
be opened::

  from pypom import Page
  from selenium.webdriver import Firefox

  class Mozilla(Page):
      URL_TEMPLATE = '/about/'

  base_url = 'https://www.mozilla.org'
  driver = Firefox()
  page = Mozilla(driver, base_url).open()

As this is a template, any additional keyword arguments passed when
instantiating the page object will attempt to resolve any placeholders. The
following example adds a locale to the URL::

  from pypom import Page
  from selenium.webdriver import Firefox

  class Mozilla(Page):
      URL_TEMPLATE = '/{locale}/about/'

  base_url = 'https://www.mozilla.org'
  driver = Firefox()
  page = Mozilla(driver, base_url, locale='de').open()

Waiting for pages to load
~~~~~~~~~~~~~~~~~~~~~~~~~

Whenever Selenium_ detects that a page is loading, it does it's best to block
until it's complete. Unfortunately, as Seleniun does not know your application,
it's quite common for it to return earlier than a user would consider the page
to be ready. For this reason, the :py:func:`pypom.page.Page.wait_for_page_to_load`
function can be overridden and customised for your project's needs by adding
suitable `explicit waits`_. This function is called by :py:func:`~pypom.page.Page.open`
after loading the seed URL, and can be called directly by functions that cause
a page to load.

The following example waits for the seed URL to be in the current URL. You can
use this so long as the URL is not rewritten or redirected by your
application::

  from pypom import Page

  class Mozilla(Page):

      def wait_for_page_to_load(self):
          self.wait.until(lambda s: self.seed_url in s.current_url)

Other things to wait for might include when elements are displayed or enabled,
or when an element has a particular class. This will be very dependent on your
application.

Regions
-------

Coming soon...

Waiting for regions to load
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coming soon...

Locators
--------

Coming soon...

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

The following example demonstrates a wait that is necessary after checking a
box that causes a button to become enabled::

  from pypom import Page
  from selenium.webdriver.common.by import By

  class Mozilla(Page):
      _privacy_policy_locator = (By.ID, 'privacy')
      _sign_me_up_locator = (By.ID, 'sign_up')

      def accept_privacy_policy(self):
          self.selenium.find_element(*self._privacy_policy_locator).click()
          sign_me_up = self.selenium.find_element(*self._sign_me_up_locator)
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
