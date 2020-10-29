import pytest

from pywappalyzer.wappalyzer import Pywappalyzer


@pytest.fixture
def wappalyzer():
    return Pywappalyzer()


@pytest.fixture
def mock_scrape_technologies_to_json(mocker):
    mock_scrape_technologies_to_json = mocker.patch(
        "pywappalyzer.wappalyzer.scrape_technologies_to_json"
    )
    mock_scrape_technologies_to_json.return_value = None
    return mock_scrape_technologies_to_json


@pytest.fixture
def mock_scrape_technologies(mocker):
    mock_scrape_technologies = mocker.patch(
        "pywappalyzer.wappalyzer.scrape_technologies"
    )
    mock_scrape_technologies.return_value = {
        "technologies": {
            "Structured\xa0Data": ["Microdata", "JSON-LD"],
            "Site\xa0Elements": [
                "IPv6",
                "HTTP Strict Transport Security",
                "QUIC",
                "HTTP/2",
                "HTTP/3",
                "Default subdomain www",
                "Default protocol https",
            ],
            "Client-side\xa0Languages": ["JavaScript", "Flash"],
            "SSL\xa0Certificate\xa0Authorities": ["GlobalSign"],
            "Web\xa0Servers": ["Google Servers"],
            "Image\xa0File\xa0Formats": ["PNG", "SVG", "JPEG", "WebP"],
            "DNS\xa0Servers": ["Google"],
            "Advertising\xa0Networks": ["Google Ads"],
            "Traffic\xa0Analysis\xa0Tools": ["Google Analytics"],
        },
        "url": "https://w3techs.com/sitesinfo?url=https://google.com",
    }
    return mock_scrape_technologies


def test_use_latest(wappalyzer: Pywappalyzer, mock_scrape_technologies_to_json):
    assert wappalyzer.use_latest() is None  # type: ignore


def test_analyze(wappalyzer: Pywappalyzer, mock_scrape_technologies):
    data = wappalyzer.analyze(url="https://google.com")
    assert data == {
        "technologies": {
            "Structured\xa0Data": ["Microdata", "JSON-LD"],
            "Site\xa0Elements": [
                "IPv6",
                "HTTP Strict Transport Security",
                "QUIC",
                "HTTP/2",
                "HTTP/3",
                "Default subdomain www",
                "Default protocol https",
            ],
            "Client-side\xa0Languages": ["JavaScript", "Flash"],
            "SSL\xa0Certificate\xa0Authorities": ["GlobalSign"],
            "Web\xa0Servers": ["Google Servers"],
            "Image\xa0File\xa0Formats": ["PNG", "SVG", "JPEG", "WebP"],
            "DNS\xa0Servers": ["Google"],
            "Advertising\xa0Networks": ["Google Ads"],
            "Traffic\xa0Analysis\xa0Tools": ["Google Analytics"],
        },
        "url": "https://w3techs.com/sitesinfo?url=https://google.com",
    }
