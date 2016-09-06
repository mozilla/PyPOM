# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random


def test_find_element_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))
    page.find_element(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_find_elements_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))
    page.find_elements(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_present_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))
    from splinter.element_list import ElementList
    from mock import Mock
    page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([Mock()])})
    assert page.is_element_present(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_present_not_present_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))
    from splinter.element_list import ElementList
    page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
    assert not page.is_element_present(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_displayed_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))

    from mock import PropertyMock
    visible_mock = PropertyMock(return_value=True)
    page.driver.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): visible_mock})
    type(getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).return_value.first).visible = visible_mock
    assert page.is_element_displayed(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])
    visible_mock.assert_called_with()


def test_is_element_displayed_not_present_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))
    from splinter.element_list import ElementList
    page.driver.configure_mock(**{'find_by_{0}.return_value'.format(splinter_strategy): ElementList([])})
    assert not page.is_element_displayed(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])


def test_is_element_displayed_not_displayed_splinter(page, splinter, splinter_strategy):
    locator = (splinter_strategy, str(random.random()))

    from mock import PropertyMock
    visible_mock = PropertyMock(return_value=False)
    page.driver.configure_mock(**{'find_by_{0}.return_value.first.visible'.format(splinter_strategy): visible_mock})
    type(getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).return_value.first).visible = visible_mock
    assert not page.is_element_displayed(*locator)
    getattr(page.driver, 'find_by_{0}'.format(splinter_strategy)).assert_called_once_with(locator[1])
    visible_mock.assert_called_with()
