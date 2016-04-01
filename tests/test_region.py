# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from mock import Mock
from pypom import Region
import pytest


class TestWaitForRegion:

    def test_wait_for_region(self, page):
        assert isinstance(Region(page).wait_for_region_to_load(), Region)

    def test_wait_for_region_timeout(self, page):
        class MyRegion(Region):
            def wait_for_region_to_load(self):
                self.wait.until(lambda s: False)
        page.timeout = 0
        from selenium.common.exceptions import TimeoutException
        with pytest.raises(TimeoutException):
            MyRegion(page)


class TestNoRoot:

    def test_root(self, page):
        assert Region(page).root is None

    def test_find_element(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        Region(page).find_element(*locator)
        selenium.find_element.assert_called_once_with(*locator)

    def test_find_elements(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        Region(page).find_elements(*locator)
        selenium.find_elements.assert_called_once_with(*locator)

    def test_is_element_displayed(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        assert Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_not_present(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        selenium.find_element.side_effect = NoSuchElementException()
        assert not Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*locator)
        selenium.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        hidden_element = selenium.find_element()
        hidden_element.is_displayed.return_value = False
        assert not Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()


class TestRootElement:

    def test_root(self, page, selenium):
        element = Mock()
        assert Region(page, root=element).root == element

    def test_find_element(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        Region(page, root=root_element).find_element(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_find_elements(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        Region(page, root=root_element).find_elements(*locator)
        root_element.find_elements.assert_called_once_with(*locator)
        selenium.find_elements.assert_not_called()

    def test_is_element_present(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        assert Region(page, root=root_element).is_element_present(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_present_not_preset(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        root_element.find_element.side_effect = NoSuchElementException()
        assert not Region(page, root=root_element).is_element_present(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_displayed(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        assert Region(page, root=root_element).is_element_displayed(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_displayed_not_present(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        root_element.find_element.side_effect = NoSuchElementException()
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        root_element.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        hidden_element = root_element.find_element()
        hidden_element.is_displayed.return_value = False
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)
        root_element.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()


class TestRootLocator:

    @pytest.fixture
    def region(self, page):
        class MyRegion(Region):
            _root_locator = (str(random.random()), str(random.random()))
        return MyRegion(page)

    def test_root(self, element, region, selenium):
        assert element == region.root
        selenium.find_element.assert_called_once_with(*region._root_locator)

    def test_find_element(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        region.find_element(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_find_elements(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        region.find_elements(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_elements.assert_called_once_with(*locator)

    def test_is_element_present(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        assert region.is_element_present(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_present_not_preset(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        element.find_element.side_effect = NoSuchElementException()
        assert not region.is_element_present(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        assert region.is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_not_present(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        element.find_element.side_effect = NoSuchElementException()
        assert not region.is_element_displayed(*locator)
        element.find_element.assert_called_once_with(*locator)
        element.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        hidden_element = element.find_element()
        hidden_element.is_displayed.return_value = False
        assert not region.is_element_displayed(*locator)
        element.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()
