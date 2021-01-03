import json
import os
import re
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs  # noqa
from bs4 import ResultSet
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.firefox.options import Options

ABS_PATH = Path(__file__).resolve().parent


def parse_cookie(cookie: str) -> dict:
    """
    Parse cookie string to dict
    :param cookie: Cookie string
    :return: Cookie's dictionary
    """
    _cookie: SimpleCookie = SimpleCookie()
    _cookie.load(cookie)

    cookies = {}
    for key, value in _cookie.items():
        cookies[key] = value

    return cookies


def read_json(path: str) -> dict:
    """
    Read json file
    :param path: File path
    :return: Dictionary from file
    """
    with open(path, "r") as f:
        data = json.load(f)
    return data


def resolve_pattern(pattern: str) -> str:
    """
    Parse regex pattern
    :param pattern: Regex pattern
    :return: Correct pattern
    """
    if ";version:" in pattern:
        _pattern = pattern.split(";version:")[0]
        return _pattern[:-1]
    return pattern


class Site:
    """
    Site interface for easy interacting with HTML/Headers etc.
    """

    def __init__(self, url: str, headers: Optional[Dict[str, Any]] = None) -> None:
        self.headers = headers
        if headers is None:
            self.headers = {
                "accept": "*/*",
                "user-agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
                ),
            }

        self.url = url
        self.js: Dict[str, Dict[str, bool]] = {}
        self.html = self.get_html()
        self.meta = {
            "html": self.html,
            "js": self.js,
            "headers": self.get_headers(),
            "host": self.get_host(),
            "styles": self.get_styles(),
            "scripts": self.get_scripts(),
        }

    def get_html(
        self, url: Optional[str] = None, *, as_text: bool = False
    ) -> Union[bytes, str]:  # pragma: no cover
        """
        Scrape site's html
        :param url: Site's url
        :param as_text: Return html as string
        :return: Site's HTML as bytes or string
        """
        if url is None:
            url = self.url

        options = Options()
        options.add_argument("--headless")
        with webdriver.Firefox(options=options) as driver:
            driver.get(url)
            page_source = driver.page_source
            self.handle_js(driver)

        if as_text:
            return page_source
        return page_source.encode("utf-8")

    def handle_js(
        self, driver: Union[webdriver.Firefox, webdriver.Chrome]
    ) -> None:  # pragma: no cover
        """
        Handle JavaScript libraries which uses the web page
        :param driver: Selenium webdriver
        """
        technologies = read_json(str(os.path.join(ABS_PATH, "db/technologies.json")))

        for technology_key in technologies.keys():
            technology = technologies[technology_key]
            js = technology.get("js")

            if js is None:
                continue

            outputs = []
            temp_: Dict[str, Dict[str, bool]] = {}
            for script, pattern in js.items():
                try:
                    output = driver.execute_script(f"return {script}")
                    if output is None:
                        output = False
                    else:
                        output = True
                    outputs.append(output)

                except JavascriptException:
                    continue

                if temp_.get(technology_key) is None:
                    temp_[technology_key] = {}

                temp_[technology_key][script] = output

            if all(outputs):
                self.js = {**self.js, **temp_}

    def get_headers(self):
        """
        Get headers from response
        :return: Response headers
        """
        with requests.Session() as session:
            response = session.get(self.url, headers=self.headers)

        return response.headers

    def _get_elements(
        self, tag: str, attrs: Optional[Dict[str, str]] = None
    ) -> ResultSet:
        """
        Parse tags from site's html
        :param tag: Needed tag
        :param attrs: Tag attributes - {"class": "SomeClass"}
        :return: List of tag elements
        """
        if attrs is None:
            attrs = {}

        soup = bs(self.html, "lxml")
        elements = soup.find_all(tag, attrs=attrs)
        return elements

    def get_styles(self) -> list:
        """
        Get tags with "link" naming
        :return: List of tag elements
        """
        result = self._get_elements(tag="link") + self._get_elements(tag="style")
        return result

    def get_host(self, url: Optional[str] = None) -> str:
        """
        Parse host of url
        :param url: Url of site
        :return: Domain from URI
        """
        if url is None:
            url = self.url

        return urlparse(url).netloc

    def get_scripts(self) -> ResultSet:
        """
        Get tags with "script" naming
        :return: List of tag elements
        """
        return self._get_elements(tag="script")


class TechnologiesProcessor:
    """
    Handle technologies on web page
    """

    def __init__(
        self,
        headers: Dict[str, Any],
        site: Site,
        technologies: Dict[str, Any],
        categories: Dict[str, Any],
    ) -> None:
        self.headers = headers
        self.technologies = technologies
        self.site = site
        self.categories = categories
        self.technologies_keys = self.technologies.keys()

    def analyze_headers(self) -> Dict[str, List[str]]:
        """
        Analyze response headers
        :return: Dictionary with matched technologies
        """
        result: Dict[str, List[str]] = {}
        headers: dict = dict(self.site.meta["headers"])  # type: ignore
        headers_json: str = json.dumps(headers)

        for technology_key in self.technologies_keys:
            technology = self.technologies[technology_key]
            cookie = technology.get("cookies")
            meta = technology.get("headers")

            if cookie is not None and headers.get("Set-Cookie") is not None:
                cookie_keys = cookie.keys()
                response_cookie = parse_cookie(headers["Set-Cookie"])

                for cookie_key in cookie_keys:
                    if cookie_key in response_cookie:
                        for cat in technology["cats"]:
                            if result.get(self.categories[str(cat)]["name"]) is None:
                                result[self.categories[str(cat)]["name"]] = []

                            result[self.categories[str(cat)]["name"]].append(
                                technology_key
                            )

            if meta is None:
                continue

            for meta_key in meta.keys():
                if headers.get(meta_key) is None:
                    continue

                pattern = resolve_pattern(pattern=meta[meta_key])
                match = re.findall(pattern, headers_json, re.I)

                if (
                    len([el for el in match if len(el) > 0]) > 0
                    or technology_key.lower() == headers[meta_key].lower()
                    or technology_key.lower() in headers[meta_key].lower()
                ):
                    for cat in technology["cats"]:
                        if result.get(self.categories[str(cat)]["name"]) is None:
                            result[self.categories[str(cat)]["name"]] = []

                        result[self.categories[str(cat)]["name"]].append(technology_key)

        return result

    def analyze_styles(self) -> Dict[str, List[str]]:
        """
        Analyze web page styles
        :return: Dictionary with matched technologies
        """
        result: Dict[str, List[str]] = {}
        styles = self.site.meta["styles"]

        for technology_key in self.technologies_keys:
            technology = self.technologies[technology_key]
            patterns = (
                technology.get("html")
                if isinstance(technology.get("html"), list)
                else [technology.get("html", "")]
            )

            for style in styles:
                for pattern in patterns:
                    _pattern = resolve_pattern(pattern=pattern)
                    try:
                        match = re.findall(_pattern, " ".join(str(style).split()), re.I)
                    except re.error:
                        continue

                    if len([el for el in match if len(el) > 0]) > 0:
                        for cat in technology["cats"]:
                            if result.get(self.categories[str(cat)]["name"]) is None:
                                result[self.categories[str(cat)]["name"]] = []

                            result[self.categories[str(cat)]["name"]].append(
                                technology_key
                            )

        return result

    def analyze_scripts(self) -> Dict[str, List[str]]:
        """
        Analyze web page scripts
        :return: Dictionary with matched technologies
        """
        result: Dict[str, List[str]] = {}
        scripts = self.site.meta["scripts"]

        for technology_key in self.technologies_keys:
            technology = self.technologies[technology_key]
            patterns = (
                technology.get("scripts")
                if isinstance(technology.get("scripts"), list)
                else [technology.get("scripts", "")]
            )

            for script in scripts:
                for pattern in patterns:
                    _pattern = resolve_pattern(pattern=pattern)
                    try:
                        match = re.findall(_pattern, str(script), re.I)
                    except re.error:
                        continue

                    if self.site.meta["js"].get(technology_key) is not None:  # type: ignore
                        for cat in technology["cats"]:
                            if result.get(self.categories[str(cat)]["name"]) is None:
                                result[self.categories[str(cat)]["name"]] = []

                            result[self.categories[str(cat)]["name"]].append(
                                technology_key
                            )

                    if len([el for el in match if len(el) > 0]) > 0:
                        for cat in technology["cats"]:
                            if result.get(self.categories[str(cat)]["name"]) is None:
                                result[self.categories[str(cat)]["name"]] = []

                            result[self.categories[str(cat)]["name"]].append(
                                technology_key
                            )

        return result

    def analyze(self) -> Dict[str, List[str]]:
        """
        Analyze technologies on web page
        :return: Dictionary with matched technologies
        """
        styles = self.analyze_styles()
        headers = self.analyze_headers()
        scripts = self.analyze_scripts()

        techs = {
            key: list(set(value))
            for key, value in {**styles, **headers, **scripts}.items()
        }
        return techs
