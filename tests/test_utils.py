from http.cookies import Morsel

import pytest
from bs4.element import Tag
from requests import Session

from pywappalyzer.utils import (
    Site,
    TechnologiesProcessor,
    parse_cookie,
    read_json,
    resolve_pattern,
)


@pytest.fixture
def site(mock_get_html, mock_handle_js):
    site = Site(url="http://python.org/")
    return site


@pytest.fixture
def technologies_processor(site, helpers):
    site.meta["headers"] = helpers.headers_msg()
    return TechnologiesProcessor(
        headers=site.headers,
        site=site,
        technologies=helpers.read_json("samples/example_technologies.json"),
        categories=helpers.read_json("samples/example_categories.json"),
    )


@pytest.fixture
def mock_requests(mocker, helpers):
    mock_requests = mocker.patch.object(Session, "get")
    mock_requests.return_value.headers = helpers.headers_msg()
    return mock_requests


@pytest.fixture
def mock_get_html(mocker, helpers):
    mock_get_html = mocker.patch.object(Site, "get_html")
    mock_get_html.return_value = helpers.read_txt(
        "samples/example_html.txt", as_bytes=True
    )
    return mock_get_html


@pytest.fixture
def mock_handle_js(mocker, helpers):
    mock_handle_js = mocker.patch.object(Site, "handle_js")
    mock_handle_js.return_value = None
    return mock_handle_js


def test_parse_cookie(helpers):
    parsed_cookie = parse_cookie(helpers.cookie_msg())
    assert isinstance(parsed_cookie["laravel_session"], Morsel)


@pytest.mark.parametrize("filename", ["samples/example.json"])
def test_read_json(helpers, filename):
    data = read_json(filename)
    expected = helpers.read_json(filename)

    assert data == expected


def test_resolve_pattern(helpers):
    pattern = resolve_pattern(helpers.pattern_msg())
    assert pattern == r"^(.+)?"

    pattern = resolve_pattern(r"^(.+)?")
    assert pattern == r"^(.+)?"


def test_site_init(site, helpers):
    assert site.html == helpers.read_txt("samples/example_html.txt", as_bytes=True)
    assert site.js == {}


def test_get_headers(site, mock_requests, helpers):
    assert site.get_headers() == helpers.headers_msg()


def test_get_styles(site):
    assert all(
        True if isinstance(element, Tag) else False for element in site.get_styles()
    )


def test_get_host(site):
    assert site.get_host(url="https://google.com") == "google.com"


def test_get_scripts(site):
    assert all(
        True if isinstance(element, Tag) else False for element in site.get_scripts()
    )


def test_technologies_processor_analyze_headers(technologies_processor, helpers):
    assert technologies_processor.analyze_headers() == helpers.analyze_headers_msg()


def test_technologies_processor_analyze_styles(technologies_processor, helpers):
    assert technologies_processor.analyze_styles() == {}


def test_technologies_processor_analyze_scripts(technologies_processor, helpers):
    result = technologies_processor.analyze_scripts()
    assert result == {
        "Analytics": ["Google Analytics", "Google Analytics"],
        "JavaScript libraries": [
            "Modernizr",
            "jQuery",
            "jQuery",
            "jQuery UI",
            "jQuery UI",
            "jQuery UI",
            "jQuery UI",
        ],
    }


def test_technologies_processor_analyze(technologies_processor, helpers):
    result = technologies_processor.analyze()
    assert helpers.sort_dict_lists(result) == helpers.sort_dict_lists(
        helpers.result_analyze_msg()
    )


def test_analyze_html(helpers):
    result = TechnologiesProcessor.analyze_html(
        html=helpers.read_txt(filename="samples/example_html.txt", as_bytes=True),
        technologies=helpers.read_json("samples/example_technologies.json"),
        categories=helpers.read_json("samples/example_categories.json"),
    )
    assert helpers.sort_dict_lists(result) == helpers.sort_dict_lists(
        {
            "Analytics": ["Google Analytics"],
            "JavaScript libraries": ["Modernizr", "jQuery UI", "jQuery"],
        }
    )
