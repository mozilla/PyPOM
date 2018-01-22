# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest

from pypom import Page


def test_base_url(base_url, page):
    assert base_url == page.seed_url


def test_seed_url_absolute(base_url, driver):
    url_template = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = url_template
    page = MyPage(driver, base_url)
    assert url_template == page.seed_url


def test_seed_url_absolute_keywords_tokens(base_url, driver):
    value = str(random.random())
    absolute_url = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = absolute_url + '{key}'
    page = MyPage(driver, base_url, key=value)
    assert absolute_url + value == page.seed_url


def test_seed_url_absolute_keywords_params(base_url, driver):
    value = str(random.random())
    absolute_url = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = absolute_url
    page = MyPage(driver, base_url, key=value)
    assert '{}?key={}'.format(absolute_url, value) == page.seed_url


def test_seed_url_absolute_keywords_tokens_and_params(base_url, driver):
    values = (str(random.random()), str(random.random()))
    absolute_url = 'https://www.test.com/'

    class MyPage(Page):
        URL_TEMPLATE = absolute_url + '?key1={key1}'
    page = MyPage(driver, base_url, key1=values[0], key2=values[1])
    assert '{}?key1={}&key2={}'.format(absolute_url, *values) == page.seed_url


def test_seed_url_empty(driver):
    page = Page(driver)
    assert page.seed_url is None


def test_seed_url_keywords_tokens(base_url, driver):
    value = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = '{key}'
    page = MyPage(driver, base_url, key=value)
    assert base_url + value == page.seed_url


def test_seed_url_keywords_params(base_url, driver):
    value = str(random.random())
    page = Page(driver, base_url, key=value)
    assert '{}?key={}'.format(base_url, value) == page.seed_url


def test_seed_url_keywords_keywords_and_params(base_url, driver):
    values = (str(random.random()), str(random.random()))

    class MyPage(Page):
        URL_TEMPLATE = '?key1={key1}'
    page = MyPage(driver, base_url, key1=values[0], key2=values[1])
    assert '{}?key1={}&key2={}'.format(base_url, *values) == page.seed_url


def test_seed_url_prepend(base_url, driver):
    url_template = str(random.random())

    class MyPage(Page):
        URL_TEMPLATE = url_template
    page = MyPage(driver, base_url)
    assert base_url + url_template == page.seed_url


def test_open(page, driver):
    assert isinstance(page.open(), Page)


def test_open_seed_url_none(driver):
    from pypom.exception import UsageError
    page = Page(driver)
    with pytest.raises(UsageError):
        page.open()


def test_open_timeout(base_url, driver):

    class MyPage(Page):
        def wait_for_page_to_load(self):
            self.wait.until(lambda s: False)
    page = MyPage(driver, base_url, timeout=0)
    from selenium.common.exceptions import TimeoutException
    with pytest.raises(TimeoutException):
        page.open()


def test_open_timeout_loaded(base_url, driver):

    class MyPage(Page):
        @property
        def loaded(self):
            return False
    page = MyPage(driver, base_url, timeout=0)
    from selenium.common.exceptions import TimeoutException
    with pytest.raises(TimeoutException):
        page.open()


def test_wait_for_page(page, driver):
    assert isinstance(page.wait_for_page_to_load(), Page)


def test_wait_for_page_timeout(base_url, driver):

    class MyPage(Page):
        def wait_for_page_to_load(self):
            self.wait.until(lambda s: False)
    page = MyPage(driver, base_url, timeout=0)
    from selenium.common.exceptions import TimeoutException
    with pytest.raises(TimeoutException):
        page.wait_for_page_to_load()


def test_wait_for_page_timeout_loaded(base_url, driver):

    class MyPage(Page):
        @property
        def loaded(self):
            return False
    page = MyPage(driver, base_url, timeout=0)
    from selenium.common.exceptions import TimeoutException
    with pytest.raises(TimeoutException):
        page.wait_for_page_to_load()


def test_wait_for_page_empty_base_url(driver):
    assert isinstance(Page(driver).wait_for_page_to_load(), Page)


def test_bwc_selenium(page, driver_interface):
    """ Backwards compatibility with old selenium attribute """
    driver = page.selenium
    assert driver == page.driver


def test_loaded(page, driver):
    assert page.loaded is True
