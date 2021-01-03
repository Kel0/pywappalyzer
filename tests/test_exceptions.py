import pytest

from pywappalyzer.exceptions import NoArgsException


def test_no_args_exception():
    error = NoArgsException("No args")
    with pytest.raises(NoArgsException):
        raise error
