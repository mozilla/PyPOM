from .page import Page  # noqa
from .region import Region  # noqa

import selenium  # noqa

# register selenium support
from .selenium_driver import register as registerSelenium
registerSelenium()

try:
    import splinter  # noqa
except ImportError:  # pragma: no cover
    pass             # pragma: no cover
else:
    from .splinter_driver import register as registerSplinter
    registerSplinter()
