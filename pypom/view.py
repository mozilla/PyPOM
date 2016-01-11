# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


class WebView(object):
    """
    The WebView class is the base for both the :class:`pypom.page.Page`
     and :class:`pypom.region.Region` classes
     """

    def __init__(self, base_url, selenium, **kwargs):
        """
        :param base_url:
            The base URL for the site on which the test is being run.

        :param selenium:
            An instance of the Selenium class.

        :param kwargs:
            Dictionary of arguments to add to the URL when generated.
        """

        self.base_url = base_url
        self.selenium = selenium
        self.wait = WebDriverWait(self.selenium, self.timeout)
        self.kwargs = kwargs

    @property
    def root(self):
        """
        The root from which Selenium commands are issued.

        Defaults to ``self.selenium`` for page objects.
        """
        return self.selenium

    @property
    def timeout(self):
        """
        The timeout, in seconds, to be used for calls to ``self.wait``.

        Defaults to ``0``.
        """
        return 0

    def find_element(self, locator):
        """
        Calls ``find_element`` on ``self.root`` which is either an instance
        of Selenium or a WebElement.

        :param locator:
            A locator that Selenium can understand.

        :returns:
            The first WebElement found using ``locator``.
        """
        return self.root.find_element(*locator)

    def find_elements(self, locator):
        """
        Calls ``find_elements`` on ``self.root`` which is either an instance
        of Selenium or a WebElement.

        :param locator:
            A locator that Selenium can understand.

        :returns:
            A list of all WebElements found using ``locator``.
        """
        return self.root.find_elements(*locator)

    def is_element_present(self, locator):
        """
        Checks whether a given element is present in the DOM.

        :param locator:
            A locator that Selenium can understand.

        :returns:
            A boolean indicating the presence of the element.
        """
        try:
            return self.find_element(locator)
        except NoSuchElementException:
            return False

    def is_element_displayed(self, locator):
        """
        Checks whether a given element is displayed in the browser.

        :param locator:
            A locator that Selenium can understand.

        :returns:
            A boolean indicating the visibility of the element.
        """
        try:
            return self.find_element(locator).is_displayed()
        except NoSuchElementException:
            return False
