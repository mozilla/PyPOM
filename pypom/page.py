# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

from .exception import UsageError
from .view import WebView

if sys.version_info >= (3,):
    from urllib.parse import urljoin
else:
    from urlparse import urljoin


class Page(WebView):

    URL_TEMPLATE = None
    """String representing a URL that will return this page.

    This string is formatted and can contain names of keyword arguments passed
    during construction of the page object. The template should either assume
    that its result will be appended to the value of ``base_url``,
    or should yield an absolute URL.
    """

    @property
    def canonical_url(self):
        """
        Returns the URL to the current page,
        formatted from :py:data:`URL_TEMPLATE`.
        Unless URL_TEMPLATE results in an absolute URL, ``self.base_url`` is
        prepended to the resulting URL.

        :returns:
            String representing a URL that will return this page.
        """
        if self.URL_TEMPLATE is not None:
            return urljoin(self.base_url,
                           self.URL_TEMPLATE.format(**self.url_kwargs))
        return self.base_url

    def find_element(self, locator):
        """
        Calls ``selenium.find_element``.

        :param locator:
            A locator that Selenium can understand.

        :returns:
            The first WebElement found using ``locator``.
        """
        return self.selenium.find_element(*locator)

    def find_elements(self, locator):
        """
        Calls ``selenium.find_elements``.

        :param locator:
            A locator that Selenium can understand.

        :returns:
            A list of all WebElements found using ``locator``.
        """
        return self.selenium.find_elements(*locator)

    def open(self):
        """
        Navigates to the URL returned by the :py:func:`canonical_url` property
        and waits for the page to load
        by calling :py:func:`wait_for_page_to_load`.

        :returns:
            The current page object (i.e., ``self``).
        """
        if self.canonical_url:
            self.selenium.get(self.canonical_url)
            self.wait_for_page_to_load()
            return self
        raise UsageError('The canonical_url for the page is empty.\n'
                         'Calling open() on the page will result in a blank'
                         'browser page and therefore does not make sense.')

    def wait_for_page_to_load(self):
        """
        Waits for the page to load by waiting until the URL reported by
        Selenium is the same as that returned by the :py:func:`canonical_url`
        property, if the :py:func:`canonical_url` property has a value.

        Note that it is common to extend or override this method
        to provide custom wait behaviour.

        :returns:
            The current page object (i.e., ``self``).
        """
        if self.canonical_url:
            self.wait.until(lambda s: self.canonical_url in s.current_url)
        return self
