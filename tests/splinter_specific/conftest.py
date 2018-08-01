# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import Mock
from zope.interface import alsoProvides

from pypom.splinter_driver import ISplinter


@pytest.fixture
def element(splinter):
    element = Mock()
    splinter.find_element.return_value = element
    return element


@pytest.fixture
def page(splinter, base_url):
    from pypom import Page

    return Page(splinter, base_url)


@pytest.fixture
def splinter():
    """ Splinter driver """
    mock = Mock()
    alsoProvides(mock, ISplinter)
    return mock
