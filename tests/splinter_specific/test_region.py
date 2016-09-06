# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from mock import (
    Mock,
    MagicMock,
    patch,
)
from pypom import Region
import pytest


class TestNoRootSplinter:

    def test_no_root_usage_error(self, page, splinter):
        locator = ('not_valid_strategy', str(random.random()))
        from pypom.exception import UsageError
        with pytest.raises(UsageError):
            Region(page).find_element(*locator)

    def test_find_element_splinter(self, page, splinter, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        from splinter.element_list import ElementList
        page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
        Region(page).find_element(*locator)
        getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_find_elements_splinter(self, page, splinter, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        from splinter.element_list import ElementList
        page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
        Region(page).find_elements(*locator)
        getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_displayed_splinter(self, page, splinter, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))

        from mock import PropertyMock
        visible_mock = PropertyMock(return_value=True)
        page.driver.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): visible_mock})
        type(getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).return_value.first).visible = visible_mock
        assert Region(page).is_element_displayed(*locator)

        getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])
        visible_mock.assert_called_with()

    def test_is_element_displayed_not_present_splinter(self, page, splinter, splinter_strategy):
        locator = (str(random.random()), str(random.random()))
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value = ElementList([])
            assert not Region(page).is_element_displayed(*locator)

    def test_is_element_displayed_hidden_splinter(self, page, splinter, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        hidden_element = splinter.find_element()
        hidden_element.is_displayed.return_value = False
        region = Region(page)
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=Mock()) as mock_find_element:
            visible_mock = Mock().visible.return_value = False
            first_mock = Mock().first.return_value = visible_mock
            mock_find_element.return_value = first_mock
            assert not region.is_element_displayed(*locator)


class TestRootElementSplinter:

    def test_no_root_usage_error(self, page, splinter):
        root_element = MagicMock()
        locator = ('not_valid_strategy', str(random.random()))
        from pypom.exception import UsageError
        with pytest.raises(UsageError):
            Region(page, root=root_element).find_element(*locator)

    def test_find_element_splinter(self, page, splinter, splinter_strategy):
        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): Mock()})
        locator = (splinter_strategy, str(random.random()))
        Region(page, root=root_element).find_element(*locator)
        getattr(root_element, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_find_elements_splinter(self, page, splinter, splinter_strategy):
        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): Mock()})
        locator = (splinter_strategy, str(random.random()))
        Region(page, root=root_element).find_elements(*locator)
        getattr(root_element, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_present_splinter(self, page, splinter, splinter_strategy):
        root_element = Mock()
        locator = (splinter_strategy, str(random.random()))
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value = ElementList([Mock()])
            assert Region(page, root=root_element).is_element_present(*locator)
            mock_find_element.assert_called_once_with(*locator, root=root_element)

    def test_is_element_present_not_preset_splinter(self, page, splinter, splinter_strategy):
        root_element = MagicMock()
        from splinter.element_list import ElementList
        root_element.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
        locator = (splinter_strategy, str(random.random()))
        assert not Region(page, root=root_element).is_element_present(*locator)

    def test_is_element_displayed_splinter(self, page, splinter, splinter_strategy):
        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): True})
        locator = (splinter_strategy, str(random.random()))
        region = Region(page, root=root_element)
        assert region.is_element_displayed(*locator)

    def test_is_element_displayed_not_present_splinter(self, page, splinter, splinter_strategy):
        root_element = Mock()
        locator = (splinter_strategy, str(random.random()))
        region = Region(page, root=root_element)
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value = ElementList([])
            assert not region.is_element_displayed(*locator)

    def test_is_element_displayed_hidden_splinter(self, page, splinter, splinter_strategy):
        root_element = MagicMock()
        root_element.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): False})
        locator = (splinter_strategy, str(random.random()))
        region = Region(page, root=root_element)
        assert not region.is_element_displayed(*locator)


class TestRootLocatorSplinter:

    @pytest.fixture
    def region(self, page, splinter_strategy):
        class MyRegion(Region):
            _root_locator = (splinter_strategy, str(random.random()))
        return MyRegion(page)

    def test_root_splinter(self, region, splinter_strategy):
        region.root
        getattr(region.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(region._root_locator[1])

    def test_find_element_splinter(self, region, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        region.find_element(*locator)

        getattr(region.root, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_find_elements_splinter(self, region, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        region.find_elements(*locator)

        getattr(region.root, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_present_splinter(self, region, splinter_strategy):
        assert region._root_locator[0] == splinter_strategy
        locator = (splinter_strategy, str(random.random()))

        assert region.is_element_present(*locator)
        getattr(region.root, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])

    def test_is_element_present_not_present_splinter(self, region, splinter_strategy):
        from splinter.element_list import ElementList
        locator = (splinter_strategy, str(random.random()))
        with patch('pypom.splinter_driver.Splinter.find_elements', new_callable=MagicMock()) as mock_find_elements:
            mock_find_elements.return_value = ElementList([])
            assert not region.is_element_present(*locator)

    def test_is_element_displayed_splinter(self, region, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=MagicMock()) as mock_find_element:
            mock_find_element.return_value.first.visible = True
            assert region.is_element_displayed(*locator)

    def test_is_element_displayed_not_present_splinter(self, region, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        from splinter.element_list import ElementList
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=Mock()) as mock_find_element:
            mock_find_element.return_value = ElementList([])
            assert not region.is_element_displayed(*locator)

    def test_is_element_displayed_hidden_splinter(self, region, splinter_strategy):
        locator = (splinter_strategy, str(random.random()))
        with patch('pypom.splinter_driver.Splinter.find_element', new_callable=Mock()) as mock_find_element:
            visible_mock = Mock().visible = False
            first_mock = Mock().first.return_value = visible_mock
            mock_find_element.return_value = first_mock
            assert not region.is_element_displayed(*locator)
