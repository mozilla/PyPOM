# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .view import WebView


class Region(WebView):
    """A page region object.

    Used as a base class for your project's page region objects.

    :param page: Page object this region appears in.
    :param root: (optional) element that serves as the root for the region.
    :type page: :py:class:`~.page.Page`
    :type root: :py:class:`~selenium.webdriver.remote.webelement.WebElement` or :py:class:`~splinter.driver.webdriver.WebDriverElement`

    Usage (Selenium)::

      from pypom import Page, Region
      from selenium.webdriver import Firefox
      from selenium.webdriver.common.by import By

      class Mozilla(Page):
          URL_TEMPLATE = 'https://www.mozilla.org/'

          @property
          def newsletter(self):
              return Newsletter(self)

          class Newsletter(Region):
              _root_locator = (By.ID, 'newsletter-form')
              _submit_locator = (By.ID, 'footer_email_submit')

              def sign_up(self):
                  self.find_element(*self._submit_locator).click()

      driver = Firefox()
      page = Mozilla(driver).open()
      page.newsletter.sign_up()

    Usage (Splinter)::

      from pypom import Page, Region
      from splinter import Browser

      class Mozilla(Page):
          URL_TEMPLATE = 'https://www.mozilla.org/'

          @property
          def newsletter(self):
              return Newsletter(self)

          class Newsletter(Region):
              _root_locator = ('id', 'newsletter-form')
              _submit_locator = ('id', 'footer_email_submit')

              def sign_up(self):
                  self.find_element(*self._submit_locator).click()

      driver = Browser()
      page = Mozilla(driver).open()
      page.newsletter.sign_up()

    """

    _root_locator = None

    def __init__(self, page, root=None):
        super(Region, self).__init__(page.driver, page.timeout)
        self._root = root
        self.page = page
        self.wait_for_region_to_load()

    @property
    def root(self):
        """Root element for the page region.

        Page regions should define a root element either by passing this on
        instantiation or by defining a :py:attr:`_root_locator` attribute. To
        reduce the chances of hitting :py:class:`~selenium.common.exceptions.StaleElementReferenceException`
        or similar you should use :py:attr:`_root_locator`, as this is looked up every
        time the :py:attr:`root` property is accessed.
        """
        if self._root is None and self._root_locator is not None:
            return self.page.find_element(*self._root_locator)
        return self._root

    def wait_for_region_to_load(self):
        """Wait for the page region to load.

        You may need to initialise your page region before it's ready for you
        to interact with it. If this is the case, you can override
        :py:func:`wait_for_region_to_load` and implement an explicit wait for a
        condition that evaluates to ``True`` when the region has finished
        loading.

        :return: The current page region object.
        :rtype: :py:class:`Region`

        Usage (Selenium)::

          from pypom import Page, Region
          from selenium.webdriver.common.by import By

          class Mozilla(Page):
              URL_TEMPLATE = 'https://www.mozilla.org/'

              @property
              def newsletter(self):
                  return Newsletter(self)

              class Newsletter(Region):
                  _root_locator = (By.ID, 'newsletter-form')

                  def wait_for_region_to_load(self):
                      self.wait.until(lambda s: 'loaded' in self.root.get_attribute('class'))

        Usage (Splinter)::

          from pypom import Page, Region

          class Mozilla(Page):
              URL_TEMPLATE = 'https://www.mozilla.org/'

              @property
              def newsletter(self):
                  return Newsletter(self)

              class Newsletter(Region):
                  _root_locator = ('id', 'newsletter-form')

                  def wait_for_region_to_load(self):
                      self.wait.until(lambda s: 'loaded' in self.root['class'])

        """
        return self

    def find_element(self, strategy, locator):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: An element.
        :rytpe: :py:class:`~selenium.webdriver.remote.webelement.WebElement` or :py:class:`~splinter.driver.webdriver.WebDriverElement`

        """
        return self.driver_adapter.find_element(strategy, locator, root=self.root)

    def find_elements(self, strategy, locator):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of :py:class:`~selenium.webdriver.remote.webelement.WebElement` or :py:class:`~splinter.element_list.ElementList`
        :rtype: list

        """
        return self.driver_adapter.find_elements(strategy, locator, root=self.root)

    def is_element_present(self, strategy, locator):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_present(strategy, locator, root=self.root)

    def is_element_displayed(self, strategy, locator):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_displayed(strategy, locator, root=self.root)
