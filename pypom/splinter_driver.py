# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from zope.interface import (
    implementer,
    Interface,
)

from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.remote import WebDriver as RemoteWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.driver.webdriver.phantomjs import WebDriver as PhantomJSWebDriver

from .interfaces import IDriver
from .driver import registerDriver
from .selenium_driver import Selenium
from .exception import UsageError

ALLOWED_STRATEGIES = [
    'name',
    'id',
    'css',
    'xpath',
    'text',
    'value',
    'tag',
]


class ISplinter(Interface):
    """ Marker interface for Splinter"""


@implementer(IDriver)
class Splinter(Selenium):

    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        """Open the page.
        Navigates to :py:attr:`url`
        """
        self.driver.visit(url)

    def find_element(self, strategy, locator, root=None):
        """Finds an element on the page.

        :param strategy: Location strategy to use. See pypom.splinter_driver.ALLOWED_STRATEGIES for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: :py:class:`~splinter.driver.webdriver.WebDriverElement`.
        :rtype: splinter.driver.webdriver.WebDriverElement

        """
        elements = self.find_elements(strategy, locator, root=root)
        return elements and elements.first or None

    def find_elements(self, strategy, locator, root=None):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See pypom.splinter_driver.ALLOWED_STRATEGIES for valid values.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of :py:class:`~splinter.driver.webdriver.WebDriverElement`
        :rtype: :py:class:`splinter.element_list.ElementList`

        """
        node = root or self.driver

        if strategy in ALLOWED_STRATEGIES:
            return getattr(node, 'find_by_' + strategy)(locator)
        raise UsageError('Strategy not allowed')

    def is_element_present(self, strategy, locator, root=None):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See pypom.splinter_driver.ALLOWED_STRATEGIES for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        return self.find_element(strategy, locator, root=root) and True or False

    def is_element_displayed(self, strategy, locator, root=None):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See pypom.splinter_driver.ALLOWED_STRATEGIES for valid values.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """

        element = self.find_element(strategy, locator, root=root)
        return element and element.visible or False


def register():
    """ Register the Selenium specific driver implementation.

        This register call is performed by the init module if
        selenium is available.
    """
    registerDriver(
        ISplinter,
        Splinter,
        class_implements=[
            FirefoxWebDriver,
            ChromeWebDriver,
            RemoteWebDriver,
            PhantomJSWebDriver,
        ])
