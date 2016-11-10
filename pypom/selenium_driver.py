# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from zope.interface import (
    implementer,
    Interface,
)

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import (
    Firefox,
    Chrome,
    Ie,
    Edge,
    Opera,
    Safari,
    BlackBerry,
    PhantomJS,
    Android,
    Remote,
)

from .interfaces import IDriver
from .driver import registerDriver


class ISelenium(Interface):
    """ Marker interface for Selenium"""


@implementer(IDriver)
class Selenium(object):

    def __init__(self, driver):
        self.driver = driver

    def wait_factory(self, timeout):
        """Returns a WebDriverWait like property for a given timeout.

        :param timeout: Timeout used by WebDriverWait calls
        :type timeout: int
        """
        return WebDriverWait(self.driver, timeout)

    def open(self, url):
        """Open the page.
        Navigates to :py:attr:`url`
        """
        self.driver.get(url)

    def find_element(self, strategy, locator, root=None):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str :py:class:`~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: :py:class:`~selenium.webdriver.remote.webelement.WebElement` object.
        :rtype: selenium.webdriver.remote.webelement.WebElement

        """
        if root is not None:
            return root.find_element(strategy, locator)
        return self.driver.find_element(strategy, locator)

    def find_elements(self, strategy, locator, root=None):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target elements.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str :py:class:`~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: List of :py:class:`~selenium.webdriver.remote.webelement.WebElement` objects.
        :rtype: list

        """
        if root is not None:
            return root.find_elements(strategy, locator)
        return self.driver.find_elements(strategy, locator)

    def is_element_present(self, strategy, locator, root=None):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str :py:class:`~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator, root=root)
        except NoSuchElementException:
            return False

    def is_element_displayed(self, strategy, locator, root=None):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` for valid values.
        :param locator: Location of target element.
        :param root: (optional) root node.
        :type strategy: str
        :type locator: str
        :type root: str :py:class:`~selenium.webdriver.remote.webelement.WebElement` object or None.
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        try:
            return self.find_element(strategy, locator, root=root).is_displayed()
        except NoSuchElementException:
            return False


def register():
    """ Register the Selenium specific driver implementation.

        This register call is performed by the init module if
        selenium is available.
    """
    registerDriver(
        ISelenium,
        Selenium,
        class_implements=[
            Firefox,
            Chrome,
            Ie,
            Edge,
            Opera,
            Safari,
            BlackBerry,
            PhantomJS,
            Android,
            Remote,
        ])
