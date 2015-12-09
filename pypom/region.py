# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from view import WebView


class PageRegion(WebView):

    _root_locator = None

    def __init__(self, page, root=None, **kwargs):
        super(PageRegion, self).__init__(page.base_url, page.selenium,
                                         **kwargs)
        self._root_element = root
        self.page = page

    @property
    def _root(self):
        if self._root_element is None:
            if self._root_locator is not None:
                return self.selenium.find_element(*self._root_locator)
            return self.selenium
        return self._root_element
