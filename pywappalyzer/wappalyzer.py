import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from .exceptions import NoArgsException
from .utils import Site, TechnologiesProcessor, read_json

ABS_PATH = Path(__file__).resolve().parent


class Pywappalyzer:
    def __init__(self):
        self.technologies = read_json(
            str(os.path.join(ABS_PATH, "db/technologies.json"))
        )
        self.categories = read_json(str(os.path.join(ABS_PATH, "db/categories.json")))

    def analyze(self, url: str) -> Dict[str, List[str]]:
        """
        Analyze technologies of web page
        :param url: Url of web site
        :return: Dictionary of technologies.
            {"Web servers": ["Nginx"], ...}
        """
        site = Site(url=url)
        if site.headers is None:
            raise NoArgsException("No site headers")

        headers: Dict[str, Any] = site.headers
        processor = TechnologiesProcessor(
            headers=headers,
            site=site,
            technologies=self.technologies,
            categories=self.categories,
        )

        return processor.analyze()

    def analyze_html(
        self, html: Optional[bytes] = None, *, file: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Analyze HTML from file or provided variable
        :param html: HTML content
        :param file: File with HTML content
        :return: Dictionary of technologies
        """
        if file:
            with open(file, "rb") as f:
                html = f.read()

        if not html and not file:
            raise NoArgsException("Provide html or file argument to function")

        result = TechnologiesProcessor.analyze_html(
            html=html, technologies=self.technologies, categories=self.categories  # type: ignore
        )
        return result

    def use(self, technologies: dict) -> None:
        """
        Use provided technologies/categories json
        """
        self.technologies = technologies["technologies"]
        self.categories = technologies["categories"]
