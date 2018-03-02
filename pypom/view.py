# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pluggy import PluginManager
from warnings import warn

from .interfaces import IDriver
from pypom import hooks


class WebView(object):

    def __init__(self, driver, timeout, pm=None):
        self.driver = driver
        self.driver_adapter = IDriver(driver)
        self.timeout = timeout
        self.pm = pm
        if self.pm is None:
            self.pm = PluginManager('pypom', implprefix='pypom_')
            self.pm.add_hookspecs(hooks)
            self.pm.load_setuptools_entrypoints('pypom.plugin')
            self.pm.check_pending()
        self.wait = self.driver_adapter.wait_factory(self.timeout)

    @property
    def selenium(self):
        """Backwards compatibility attribute"""
        warn('use driver instead', DeprecationWarning)
        return self.driver

    def find_element(self, strategy, locator):
        return self.driver_adapter.find_element(strategy, locator)

    def find_elements(self, strategy, locator):
        """Finds elements on the page.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target elements.
        :type strategy: str
        :type locator: str
        :return: List of :py:class:`~selenium.webdriver.remote.webelement.WebElement` or :py:class:`~splinter.element_list.ElementList`
        :rtype: list

        """
        return self.driver_adapter.find_elements(strategy, locator)

    def is_element_present(self, strategy, locator):
        """Checks whether an element is present.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is present, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_present(strategy, locator)

    def is_element_displayed(self, strategy, locator):
        """Checks whether an element is displayed.

        :param strategy: Location strategy to use. See :py:class:`~selenium.webdriver.common.by.By` or :py:attr:`~pypom.splinter_driver.ALLOWED_STRATEGIES`.
        :param locator: Location of target element.
        :type strategy: str
        :type locator: str
        :return: ``True`` if element is displayed, else ``False``.
        :rtype: bool

        """
        return self.driver_adapter.is_element_displayed(strategy, locator)
