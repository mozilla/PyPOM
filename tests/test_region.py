# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from mock import Mock
from pypom import Region


def test_root_selenium(page, selenium):
    assert Region(page).root == selenium


def test_root_element(page, selenium):
    element = Mock()
    assert Region(page, root=element).root == element


def test_root_locator(page, selenium):
    element = Mock()
    selenium.find_element.return_value = element
    locator = (str(random.random()), str(random.random()))
    region = Region(page)
    region._root_locator = locator
    assert element == region.root
    selenium.find_element.assert_called_once_with(*locator)


def test_find_element_without_root(page, selenium):
    locator = (str(random.random()), str(random.random()))
    Region(page).find_element(locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_find_elements_without_root(page, selenium):
    locator = (str(random.random()), str(random.random()))
    Region(page).find_elements(locator)
    selenium.find_elements.assert_called_once_with(*locator)


def test_find_element_with_root_element(page, selenium):
    root_element = Mock()
    locator = (str(random.random()), str(random.random()))
    Region(page, root=root_element).find_element(locator)
    root_element.find_element.assert_called_once_with(*locator)
    selenium.find_element.assert_not_called()


def test_find_elements_with_root_element(page, selenium):
    root_element = Mock()
    locator = (str(random.random()), str(random.random()))
    Region(page, root=root_element).find_elements(locator)
    root_element.find_elements.assert_called_once_with(*locator)
    selenium.find_elements.assert_not_called()


def test_find_element_with_root_locator(page, selenium):
    root_locator = (str(random.random()), str(random.random()))
    root_element = Mock()
    selenium.find_element.return_value = root_element
    region = Region(page)
    region._root_locator = root_locator
    element_locator = (str(random.random()), str(random.random()))
    region.find_element(element_locator)
    selenium.find_element.assert_called_once_with(*root_locator)
    root_element.find_element.assert_called_once_with(*element_locator)


def test_find_elements_with_root_locator(page, selenium):
    root_locator = (str(random.random()), str(random.random()))
    root_element = Mock()
    selenium.find_element.return_value = root_element
    region = Region(page)
    region._root_locator = root_locator
    elements_locator = (str(random.random()), str(random.random()))
    region.find_elements(elements_locator)
    selenium.find_element.assert_called_once_with(*root_locator)
    root_element.find_elements.assert_called_once_with(*elements_locator)


# TODO make the following tests region specific

def test_is_element_present(page, selenium):
    locator = (str(random.random()), str(random.random()))
    assert page.is_element_present(locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_is_element_present_not_present(page, selenium):
    locator = (str(random.random()), str(random.random()))
    from selenium.common.exceptions import NoSuchElementException
    selenium.find_element.side_effect = NoSuchElementException()
    assert not page.is_element_present(locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_is_element_displayed(page, selenium):
    locator = (str(random.random()), str(random.random()))
    assert page.is_element_displayed(locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_is_element_displayed_not_present(page, selenium):
    locator = (str(random.random()), str(random.random()))
    from selenium.common.exceptions import NoSuchElementException
    selenium.find_element.side_effect = NoSuchElementException()
    assert not page.is_element_displayed(locator)
    selenium.find_element.assert_called_once_with(*locator)
    selenium.find_element.is_displayed.assert_not_called()


def test_is_element_displayed_not_displayed(page, selenium):
    locator = (str(random.random()), str(random.random()))
    element = selenium.find_element()
    element.is_displayed.return_value = False
    assert not page.is_element_displayed(locator)
    selenium.find_element.assert_called_with(*locator)
    element.is_displayed.assert_called_once_with()
