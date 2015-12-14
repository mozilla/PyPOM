# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .view import WebView


class Page(WebView):

    _url = None
    """
    A string which when appended to ``base_url``
    indicates the url to the given page.

    Defaults to ``None``.
    """

    def open(self):
        """
        Navigates to the url returned by the :py:func:`url` property and
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
        Returns the url to the current page, which is either built from
        the private :py:data:`_url` variable if populated or is ``base_url``.

        :returns:
            The url to the current page.
        """
        if self._url is not None:
            return self._url.format(base_url=self.base_url, **self.kwargs)
        return self.base_url

    def wait_for_page_to_load(self):
        """
        Waits for the page to load by waiting until the url reported by
        Selenium is the same as that returned by the :py:func:`url` property.

        Note that it is common to extend or override this method
        to provide custom wait behaviour.

        :returns:
            The current page object (i.e., ``self``).
        """
        self.wait.until(lambda s: self.url in s.current_url)
        return self
