# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from mock import (
    Mock,
)

from pypom import Region


class TestWaitForRegion:

    def test_wait_for_region(self, page):
        assert isinstance(Region(page).wait_for_region_to_load(), Region)

    def test_wait_for_region_timeout(self, page):

        class MyRegion(Region):
            def wait_for_region_to_load(self):
                self.wait.until(lambda s: False)
        page.timeout = 0
        from selenium.common.exceptions import TimeoutException
        with pytest.raises(TimeoutException):
            MyRegion(page)


class TestNoRoot:

    def test_root(self, page):
        assert Region(page).root is None


class TestRootElement:

    def test_root(self, page, driver):
        element = Mock()
        assert Region(page, root=element).root == element
