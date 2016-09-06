# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def test_register_driver():
    """ We are testing the registerDriver hook"""
    import pytest
    from zope.interface import implementer
    from zope.interface import Interface
    from pypom.driver import registerDriver
    from pypom.interfaces import IDriver

    class IFakeDriver(Interface):
        """ A fake marker interface"""

    @implementer(IFakeDriver)
    class FakeDriver:
        """ A fake driver """
        def __init__(self, driver):
            self.driver = driver

    fake_driver = FakeDriver(None)

    # no register driver, look up error
    with pytest.raises(TypeError):
        IDriver(fake_driver)

    registerDriver(IFakeDriver, FakeDriver)

    # driver implementation available after registerDriver
    adapted_driver = IDriver(fake_driver)

    # same instance of adapted_driver
    assert isinstance(adapted_driver, FakeDriver)


def test_multiple_register_driver():
    """ We are testing the registerDriver hook,
        multiple registrations"""
    from zope.interface import implementer
    from zope.interface import Interface
    from pypom.driver import registerDriver
    from pypom.interfaces import IDriver

    class IFakeDriver(Interface):
        """ A fake marker interface"""

    @implementer(IFakeDriver)
    class FakeDriver:
        """ A fake driver """
        def __init__(self, driver):
            self.driver = driver

    class IFakeDriver2(Interface):
        """ Another fake marker interface"""

    @implementer(IFakeDriver2)
    class FakeDriver2:
        """ Another fake driver """
        def __init__(self, driver):
            self.driver = driver

    fake_driver = FakeDriver(None)
    fake_driver2 = FakeDriver2(None)

    registerDriver(IFakeDriver, FakeDriver)
    registerDriver(IFakeDriver2, IFakeDriver2)

    # driver implementation available after registerDriver
    adapted_driver = IDriver(fake_driver)
    adapted_driver2 = IDriver(fake_driver2)

    # same instance of adapted_driver
    assert isinstance(adapted_driver, FakeDriver)
    assert isinstance(adapted_driver2, FakeDriver2)


def test_register_driver_class_implements():
    """ We are testing the registerDriver hook with
        class implements"""
    from zope.interface import Interface
    from pypom.driver import registerDriver
    from pypom.interfaces import IDriver

    class IFakeDriver(Interface):
        """ A fake marker interface"""

    class FakeDriver:
        """ A fake driver """
        def __init__(self, driver):
            self.driver = driver

    fake_driver = FakeDriver(None)

    registerDriver(IFakeDriver, FakeDriver, [FakeDriver])

    # driver implementation available after registerDriver
    adapted_driver = IDriver(fake_driver)

    # same instance of adapted_driver
    assert isinstance(adapted_driver, FakeDriver)
