# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest
from mock import (
    Mock,
)

from pypom import Region


class TestNoRoot:

    def test_find_element_selenium(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        Region(page).find_element(*locator)
        selenium.find_element.assert_called_once_with(*locator)

    def test_find_elements_selenium(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        Region(page).find_elements(*locator)
        selenium.find_elements.assert_called_once_with(*locator)

    def test_is_element_displayed_selenium(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        assert Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_not_present_selenium(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        selenium.find_element.side_effect = NoSuchElementException()
        assert not Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*locator)
        selenium.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden_selenium(self, page, selenium):
        locator = (str(random.random()), str(random.random()))
        hidden_element = selenium.find_element()
        hidden_element.is_displayed.return_value = False
        assert not Region(page).is_element_displayed(*locator)
        selenium.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()


class TestRootElement:

    def test_find_element_selenium(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        Region(page, root=root_element).find_element(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_find_elements_selenium(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        Region(page, root=root_element).find_elements(*locator)
        root_element.find_elements.assert_called_once_with(*locator)
        selenium.find_elements.assert_not_called()

    def test_is_element_present_selenium(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        assert Region(page, root=root_element).is_element_present(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_present_not_preset_selenium(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        root_element.find_element.side_effect = NoSuchElementException()
        assert not Region(page, root=root_element).is_element_present(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_displayed_selenium(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        assert Region(page, root=root_element).is_element_displayed(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        selenium.find_element.assert_not_called()

    def test_is_element_displayed_not_present_selenium(self, page, selenium):
        root_element = Mock()
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        root_element.find_element.side_effect = NoSuchElementException()
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)
        root_element.find_element.assert_called_once_with(*locator)
        root_element.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden_selenium(self, page, selenium):
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

    def test_root_selenium(self, element, region, selenium):
        assert element == region.root
        selenium.find_element.assert_called_once_with(*region._root_locator)

    def test_find_element_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        region.find_element(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_find_elements_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        region.find_elements(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_elements.assert_called_once_with(*locator)

    def test_is_element_present_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        assert region.is_element_present(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_present_not_present_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        element.find_element.side_effect = NoSuchElementException()
        assert not region.is_element_present(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        assert region.is_element_displayed(*locator)
        selenium.find_element.assert_called_once_with(*region._root_locator)
        element.find_element.assert_called_once_with(*locator)

    def test_is_element_displayed_not_present_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        from selenium.common.exceptions import NoSuchElementException
        element.find_element.side_effect = NoSuchElementException()
        assert not region.is_element_displayed(*locator)
        element.find_element.assert_called_once_with(*locator)
        element.find_element.is_displayed.assert_not_called()

    def test_is_element_displayed_hidden_selenium(self, element, region, selenium):
        locator = (str(random.random()), str(random.random()))
        hidden_element = element.find_element()
        hidden_element.is_displayed.return_value = False
        assert not region.is_element_displayed(*locator)
        element.find_element.assert_called_with(*locator)
        hidden_element.is_displayed.assert_called_once_with()
