# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from mock import Mock
import pytest


@pytest.fixture
def base_url():
    return str(random.random())


@pytest.fixture
def page(base_url, selenium):
    from pypom import Page
    return Page(base_url, selenium)


@pytest.fixture
def selenium():
    return Mock()
