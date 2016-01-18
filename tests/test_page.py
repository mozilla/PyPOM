# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest

from pypom import Page


def test_base_url(base_url, page):
    assert base_url == page.canonical_url


def test_canonical_url_absolute(base_url, selenium):
    url_template = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = url_template
    page = MyPage(selenium, base_url)
    assert url_template == page.canonical_url


def test_canonical_url_absolute_keywords(base_url, selenium):
    value = str(random.random())
    absolute_url = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = absolute_url + '{key}'
    page = MyPage(selenium, base_url, key=value)
    assert absolute_url + value == page.canonical_url


def test_canonical_url_empty(selenium):
    page = Page(selenium)
    assert page.canonical_url is None


def test_canonical_url_keywords(base_url, selenium):
    value = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = '{key}'
    page = MyPage(selenium, base_url, key=value)
    assert base_url + value == page.canonical_url


def test_canonical_url_prepend(base_url, selenium):
    url_template = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = url_template
    page = MyPage(selenium, base_url)
    assert base_url + url_template == page.canonical_url


def test_open(page, selenium):
    selenium.current_url = page.canonical_url
    assert isinstance(page.open(), Page)


def test_open_canonical_url_none(selenium):
    from pypom.exception import UsageError
    page = Page(selenium)
    with pytest.raises(UsageError):
        page.open()


def test_open_timeout(page, selenium):
    from selenium.common.exceptions import TimeoutException
    selenium.current_url = str(random.random())
    with pytest.raises(TimeoutException):
        page.open()


def test_wait_for_page(page, selenium):
    selenium.current_url = page.canonical_url
    assert isinstance(page.wait_for_page_to_load(), Page)


def test_wait_for_page_timeout(page, selenium):
    from selenium.common.exceptions import TimeoutException
    selenium.current_url = str(random.random())
    with pytest.raises(TimeoutException):
        page.wait_for_page_to_load()


def test_wait_for_page_empty_base_url(selenium):
    selenium.current_url = str(random.random())
    page = Page(selenium)
    assert isinstance(page.wait_for_page_to_load(), Page)


def test_find_element(page, selenium):
    locator = (str(random.random()), str(random.random()))
    page.find_element(locator)
    selenium.find_element.assert_called_once_with(*locator)


def test_find_elements(page, selenium):
    locator = (str(random.random()), str(random.random()))
    page.find_elements(locator)
    selenium.find_elements.assert_called_once_with(*locator)


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
