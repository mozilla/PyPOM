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
    :type root: :py:class:`~selenium.webdriver.remote.webelement.WebElement`

    Usage::

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

    """

    def __init__(self, page, root=None):
        super(Region, self).__init__(page.selenium, page.timeout)
        self._root = root
        self._root_locator = None
        self.page = page

    @property
    def root(self):
        """Root element for the page region.

        Page regions should define a root element either by passing this on
        instantiation or by defining a :py:attr:`_root_locator` attribute. To
        reduce the chances of hitting :py:class:`~selenium.common.exceptions.StaleElementReferenceException`
        you should use :py:attr:`_root_locator`, as this is looked up every
        time the :py:attr:`root` property is accessed.
        """
        if self._root is None and self._root_locator is not None:
            return self.page.find_element(*self._root_locator)
        return self._root
