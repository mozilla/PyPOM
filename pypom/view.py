# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


class WebView(object):

    def __init__(self, selenium, timeout):
        self.selenium = selenium
        self.timeout = timeout
        self.wait = WebDriverWait(self.selenium, self.timeout)

    def find_element(self, strategy, locator):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: :py:class:`~selenium.webdriver.remote.webelement.WebElement` object.
        :rtype: selenium.webdriver.remote.webelement.WebElement

        """
        from pypom import Region
        if isinstance(self, Region):
            root = self.root
            if root is not None:
                return root.find_element(strategy, locator)
        return self.selenium.find_element(strategy, locator)

    def find_elements(self, strategy, locator):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of :py:class:`~selenium.webdriver.remote.webelement.WebElement` objects.
        :rtype: list

        """
        from pypom import Region
        if isinstance(self, Region):
            root = self.root
            if root is not None:
                return root.find_elements(strategy, locator)
        return self.selenium.find_elements(strategy, locator)

    def is_element_present(self, strategy, locator):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator)
        except NoSuchElementException:
            return False

    def is_element_displayed(self, strategy, locator):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator).is_displayed()
        except NoSuchElementException:
            return False
