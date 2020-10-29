import pytest

from pywappalyzer.scraper import (  # isort:skip
    get_html,
    parse_technologies_html,
    read_technologies_json,
    scrape_technologies,
    scrape_technologies_to_json,
    write_json,
)


@pytest.fixture
def mock_open(mocker):
    mock_open = mocker.patch("pywappalyzer.scraper.open")
    mock_open.dump.return_value = None
    return mock_open


@pytest.fixture
def mock_requests(mocker, helpers):
    mock_requests = mocker.patch("pywappalyzer.scraper.requests")
    mock_requests.get.return_value.content = helpers.txt_to_bytes(
        filename="samples/get_html_sample.txt"
    )
    return mock_requests


def test_write_json(mock_open):
    assert write_json(filename="Some file", data={}) is None


def test_read_technologies_json(helpers):
    data = read_technologies_json(filename="samples/technologies.json")
    expected_out = helpers.read_json(filename="samples/technologies_list.json")

    assert data == expected_out


def test_get_html(mock_requests, helpers):
    data = get_html("https://w3techs.com/technologies/overview/content_management")

    assert data == helpers.txt_to_bytes("samples/get_html_sample.txt")


def test_parse_technologies_html(helpers):
    content = helpers.txt_to_bytes("samples/get_html_sample.txt")
    data = parse_technologies_html(content=content)

    assert data == helpers.technologies_msg(
        filename="samples/technologies_list_array.json"
    )


def test_scrape_technologies(mock_requests, helpers):
    mock_requests.get.return_value.content = helpers.txt_to_bytes(
        "samples/get_html_scrape_technologies.txt"
    )
    data = scrape_technologies(
        url="https://w3techs.com/sitesinfo?url=https://google.com"
    )

    assert helpers.sort_dict_lists(data) == helpers.sort_dict_lists(
        {
            "technologies": {
                "Image\xa0File\xa0Formats": ["SVG", "GIF", "PNG"],
                "Site\xa0Elements": ["Default protocol https"],
                "Email\xa0Servers": ["Fastmail", "Hetzner"],
                "Traffic\xa0Analysis\xa0Tools": ["Matomo"],
                "SSL\xa0Certificate\xa0Authorities": ["IdenTrust"],
                "Structured\xa0Data": ["JSON-LD"],
                "Social\xa0Widgets": ["Twitter", "LinkedIn"],
                "Client-side\xa0Languages": ["JavaScript"],
            },
            "url": "https://w3techs.com/sitesinfo?url=https://w3techs.com/sitesinfo?url=https://google.com",
        }
    )


def test_scrape_technologies_to_json(mock_open, mock_requests):
    assert scrape_technologies_to_json() is None
