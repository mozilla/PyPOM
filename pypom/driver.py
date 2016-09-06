# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from zope import component
from zope.interface import classImplements
from .interfaces import IDriver


def registerDriver(iface, driver, class_implements=[]):
    """ Register driver adapter used by page object"""
    for class_item in class_implements:
        classImplements(class_item, iface)

    component.provideAdapter(
        factory=driver, adapts=[iface],
        provides=IDriver)
