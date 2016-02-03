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

    def __init__(self, selenium, base_url=None, timeout=10, **url_kwargs):
        """
        :param selenium:
            An instance of the Selenium class.

        :param base_url:
            The base URL for the site on which the test is being run.

            Defaults to ``None``.

        :param timeout:
            The timeout, in seconds, to be used for calls to ``self.wait``.

            Defaults to ``10``.

        :param url_kwargs:
            Dictionary of arguments to add to the URL when generated.
        """

        self.selenium = selenium
        self.base_url = base_url
        self.timeout = timeout
        self.wait = WebDriverWait(self.selenium, self.timeout)
        self.url_kwargs = url_kwargs

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
