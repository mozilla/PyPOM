# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

from .exception import UsageError
from .view import WebView

if sys.version_info >= (3,):
    import urllib.parse as urlparse
    from urllib.parse import urlencode
else:
    import urlparse
    from urllib import urlencode


class Page(WebView):
    """A page object.

    Used as a base class for your project's page objects.

    :param driver: A driver.
    :param base_url: (optional) Base URL.
    :param timeout: (optional) Timeout used for explicit waits. Defaults to ``10``.
    :param url_kwargs: (optional) Keyword arguments used when generating the :py:attr:`seed_url`.
    :type driver: :py:class:`~selenium.webdriver.remote.webdriver.WebDriver` or :py:class:`~splinter.browser.Browser`
    :type base_url: str
    :type timeout: int

    Usage (Selenium)::

      from pypom import Page
      from selenium.webdriver import Firefox

      class Mozilla(Page):
          URL_TEMPLATE = 'https://www.mozilla.org/{locale}'

      driver = Firefox()
      page = Mozilla(driver, locale='en-US')
      page.open()

    Usage (Splinter)::

      from pypom import Page
      from splinter import Browser

      class Mozilla(Page):
          URL_TEMPLATE = 'https://www.mozilla.org/{locale}'

      driver = Browser()
      page = Mozilla(driver, locale='en-US')
      page.open()

    """

    URL_TEMPLATE = None
    """Template string representing a URL that can be used to open the page.

    This string is formatted and can contain names of keyword arguments passed
    during construction of the page object. The template should either assume
    that its result will be appended to the value of :py:attr:`base_url`, or
    should yield an absolute URL.

    Examples::

        URL_TEMPLATE = 'https://www.mozilla.org/'  # absolute URL
        URL_TEMPLATE = '/search'  # relative to base URL
        URL_TEMPLATE = '/search?q={term}'  # keyword argument expansion

    """

    def __init__(self, driver, base_url=None, timeout=10, **url_kwargs):
        super(Page, self).__init__(driver, timeout)
        self.base_url = base_url
        self.url_kwargs = url_kwargs

    @property
    def seed_url(self):
        """A URL that can be used to open the page.

        The URL is formatted from :py:attr:`URL_TEMPLATE`, which is then
        appended to :py:attr:`base_url` unless the template results in an
        absolute URL.

        :return: URL that can be used to open the page.
        :rtype: str

        """
        url = self.base_url
        if self.URL_TEMPLATE is not None:
            url = urlparse.urljoin(self.base_url,
                                   self.URL_TEMPLATE.format(**self.url_kwargs))

        if not url:
            return None

        params = {}
        for k, v in self.url_kwargs.items():
            if '{{{}}}'.format(k) not in str(self.URL_TEMPLATE):
                params[k] = v

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)
        return urlparse.urlunparse(url_parts)

    def open(self):
        """Open the page.

        Navigates to :py:attr:`seed_url` and calls :py:func:`wait_for_page_to_load`.

        :return: The current page object.
        :rtype: :py:class:`Page`
        :raises: UsageError

        """
        if self.seed_url:
            self.driver_adapter.open(self.seed_url)
            self.wait_for_page_to_load()
            return self
        raise UsageError('Set a base URL or URL_TEMPLATE to open this page.')

    def wait_for_page_to_load(self):
        """Wait for the page to load."""
        self.wait.until(lambda _: self.loaded)
        self.pm.hook.pypom_after_wait_for_page_to_load(page=self)
        return self

    @property
    def loaded(self):
        """Loaded state of the page.

        By default the driver will try to wait for any page loads to be
        complete, however it's not uncommon for it to return early. To address
        this you can override :py:attr:`loaded` to return ``True`` when the
        page has finished loading.

        :return: ``True`` if page is loaded, else ``False``.
        :rtype: bool

        Usage (Selenium)::

          from pypom import Page
          from selenium.webdriver.common.by import By

          class Mozilla(Page):

              @property
              def loaded(self):
                  body = self.find_element(By.TAG_NAME, 'body')
                  return 'loaded' in body.get_attribute('class')

        Usage (Splinter)::

          from pypom import Page

          class Mozilla(Page):

              def loaded(self):
                  body = self.find_element('tag', 'body')
                  return 'loaded' in body['class']

        Examples::

            # wait for the seed_url value to be in the current URL
            self.seed_url in self.selenium.current_url

        """
        return True
