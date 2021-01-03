from platform import platform

import geckodriver_autoinstaller

from .utils import Site, TechnologiesProcessor  # noqa: F841,F401
from .wappalyzer import Pywappalyzer  # noqa: F841,F401

if "windows" in platform().lower():
    geckodriver_autoinstaller.install()
