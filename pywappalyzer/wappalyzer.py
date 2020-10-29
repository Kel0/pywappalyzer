from typing import Dict, List, Union

from .scraper import scrape_technologies, scrape_technologies_to_json


class Pywappalyzer:  # noqa
    def use_latest(self) -> None:
        scrape_technologies_to_json()

    def analyze(self, url: str) -> Dict[str, Union[str, Dict[str, List[str]]]]:
        technologies = scrape_technologies(url=url)
        return technologies
