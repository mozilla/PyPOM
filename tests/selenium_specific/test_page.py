# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random


def test_find_element_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    page.find_element(*locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_find_elements_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    page.find_elements(*locator)
    selenium.find_elements.assert_called_once_with(*locator)


def test_is_element_present_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    assert page.is_element_present(*locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_is_element_present_not_present_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    from selenium.common.exceptions import NoSuchElementException
    selenium.find_element.side_effect = NoSuchElementException()
    assert not page.is_element_present(*locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_is_element_displayed_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    assert page.is_element_displayed(*locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_is_element_displayed_not_present_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    from selenium.common.exceptions import NoSuchElementException
    selenium.find_element.side_effect = NoSuchElementException()
    assert not page.is_element_displayed(*locator)
    selenium.find_element.assert_called_once_with(*locator)
    selenium.find_element.is_displayed.assert_not_called()


def test_is_element_displayed_not_displayed_selenium(page, selenium):
    locator = (str(random.random()), str(random.random()))
    element = selenium.find_element()
    element.is_displayed.return_value = False
    assert not page.is_element_displayed(*locator)
    selenium.find_element.assert_called_with(*locator)
    element.is_displayed.assert_called_once_with()
