from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from pywappalyzer.wappalyzer import Pywappalyzer


@dataclass
class Site:
    headers: dict


@pytest.fixture
def pywappalyzer():
    return Pywappalyzer()


@pytest.fixture
def mock_site(mocker):
    mock_site = mocker.patch("pywappalyzer.wappalyzer.Site")
    mock_site.return_value = Site(headers={})
    return mock_site


@pytest.fixture
def mock_open(mocker):
    mock_open = mocker.patch("builtins.open")
    mock_open.return_value.truncate.return_value = None
    return mock_open


@pytest.fixture
def mock_json(mocker):
    mock_json = mocker.patch("pywappalyzer.wappalyzer.json")
    mock_json.dump.return_value = None
    return mock_json


@pytest.fixture
def mock_requests_get():
    mock_requests_get = Mock()
    mock_requests_get.json.return_value = {"categories": {}, "technologies": {}}
    return mock_requests_get


@pytest.fixture
def mock_requests(mocker, mock_requests_get):
    mock_requests = mocker.patch("pywappalyzer.wappalyzer.requests")
    mock_requests.get.return_value = mock_requests_get
    return mock_requests_get


@pytest.fixture
def mock_technologies_processor(mocker, helpers):
    mock_technologies_processor = mocker.patch(
        "pywappalyzer.wappalyzer.TechnologiesProcessor"
    )
    mock_technologies_processor.return_value.analyze.return_value = (
        helpers.result_analyze_msg()
    )
    return mock_technologies_processor


def test_analyze(pywappalyzer, mock_site, mock_technologies_processor):
    result = pywappalyzer.analyze(url="https://python.org/")
    assert result == {
        "Web frameworks": ["Laravel"],
        "Web servers": ["Nginx"],
        "Reverse proxies": ["Nginx"],
        "Caching": ["Varnish"],
        "Analytics": ["Google Analytics"],
        "JavaScript libraries": ["jQuery", "jQuery UI", "Modernizr"],
    }


def test_use_latest(pywappalyzer, mock_json, mock_open, mock_requests):
    pywappalyzer.use_latest()
