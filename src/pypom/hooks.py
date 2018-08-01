# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pluggy import HookspecMarker

hookspec = HookspecMarker('pypom')


@hookspec
def pypom_after_wait_for_page_to_load(page):
    """Called after waiting for the page to load"""


@hookspec
def pypom_after_wait_for_region_to_load(region):
    """Called after waiting for the region to load"""
