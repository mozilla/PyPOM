# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .view import WebView


class Region(WebView):

    _root_locator = None
    """
    A Selenium locator that will return a WebElement which should
    serve as the root element for this Region.

    Defaults to ``None``.
    """

    def __init__(self, page, root=None):
        """
        :param page:
            The page object in which this Region is contained.

        :param root:
            WebElement from which Selenium find commands will
            operate for this Region.

            Defaults to ``None`` which results in the root being Selenium.
        """
        super(Region, self).__init__(page.selenium,
                                     page.base_url,
                                     page.timeout)
        self._root_element = root
        self.page = page

    @property
    def root(self):
        """
        Returns the root from which Selenium find commands will
        operate for this Region.

        If a ``root`` was passed into the constructor,
        that element will be returned as the root.
        If a locator was specified in :py:data:`_root_locator`,
        the element found using that locator will be returned as the root.
        If neither of those are true,
        then Selenium will be returned as the root.
        """
        if self._root_element is None:
            if self._root_locator is not None:
                return self.selenium.find_element(*self._root_locator)
            return self.selenium
        return self._root_element

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
