# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import Mock
import pytest
from pypom.selenium_driver import ISelenium
from zope.interface import alsoProvides


@pytest.fixture
def element(selenium):
    element = Mock()
    selenium.find_element.return_value = element
    return element


@pytest.fixture
def page(selenium, base_url):
    from pypom import Page
    return Page(selenium, base_url)


@pytest.fixture
def selenium():
    """ Selenium driver """
    mock = Mock()
    alsoProvides(mock, ISelenium)
    return mock
