# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region, hookimpl


def test_after_wait_for_page_to_load(page):
    log = []

    class Plugin:
        @hookimpl
        def pypom_after_wait_for_page_to_load(self, page):
            log.append(1)

        @hookimpl
        def pypom_after_wait_for_region_to_load(self, region):
            log.append(2)

    page.pm.register(Plugin())
    page.open()
    Region(page)
    assert log == [1, 2]
