# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .view import WebView


class Page(WebView):

    _url = '{base_url}'
    """String representing a URL that will return this page.

    This string is formatted and can contain names of keyword arguments passed
    during construcion of the page object. The ``{base_url}`` keyword argument
    is always passed to the format operation.
    """

    def open(self):
        """
        Navigates to the URL returned by the :py:func:`url` property and
        waits for the page to load by calling :py:func:`wait_for_page_to_load`.

        :returns:
            The current page object (i.e., ``self``).
        """
        self.selenium.get(self.url)
        self.wait_for_page_to_load()
        return self

    @property
    def url(self):
        """
        Returns the URL to the current page, formatted from :py:data:`_url`.

        :returns:
            String representing a URL that will return this page.
        """
        return self._url.format(base_url=self.base_url, **self.kwargs)

    def wait_for_page_to_load(self):
        """
        Waits for the page to load by waiting until the URL reported by
        Selenium is the same as that returned by the :py:func:`url` property.

        Note that it is common to extend or override this method
        to provide custom wait behaviour.

        :returns:
            The current page object (i.e., ``self``).
        """
        self.wait.until(lambda s: self.url in s.current_url)
        return self
