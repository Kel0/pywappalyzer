import json
from pathlib import Path
from typing import Dict, List, Union

import requests
from bs4 import BeautifulSoup as bs

SITE_LINK = "https://w3techs.com/sitesinfo?url={}"
TECHNOLOGIES_LINK = "https://w3techs.com/technologies"
HEADERS = {
    "accept": "*/*",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    ),
}

FILE_PATH = Path(__file__).parent.absolute()


def write_json(filename: str, data: dict) -> None:
    with open(filename, "w+") as f:
        json.dump(data, f, ensure_ascii=True, indent=4)


def read_technologies_json(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)

    technologies = {}
    for tech in list(data.keys()):
        element = data[tech]

        for el in element:
            technologies[el] = tech

    return technologies


def get_html(url: str) -> bytes:
    response: requests.Response = requests.get(url=url, headers=HEADERS)
    return response.content


def parse_technologies_html(content: bytes) -> List[str]:
    soup = bs(content, "lxml")
    bars = soup.find("table", attrs={"class": "bars"})
    trs = bars.find_all("tr")
    ul_techs = [tech.text for tech in soup.find("ul").find_all("li")]
    technologies = []

    for tr in trs[3:]:
        tech = tr.find_all("th")
        if len(tech) > 0:
            technologies.append(tech[0].text)

    return technologies + ul_techs


def scrape_technologies(url: str) -> Dict[str, Union[str, Dict[str, List[str]]]]:
    result: Dict[str, Union[str, Dict[str, List[str]]]] = {"technologies": {}}
    html = get_html(url=SITE_LINK.format(url))
    soup = bs(html, "lxml")
    technologies_json = read_technologies_json(f"{FILE_PATH}/db/technologies.json")
    tech_table = soup.find("td", attrs={"class": "tech_main"})
    technologies = tech_table.find_all("p", attrs={"class": "si_tech"})

    result["url"] = SITE_LINK.format(url)
    technology_names = {technology.find("a").text for technology in technologies}
    technologies_dict: Dict[str, List[str]] = result["technologies"]  # type: ignore

    for technology_name in technology_names:

        if not technologies_json.get(technology_name):
            continue

        if technologies_json[technology_name] in result["technologies"]:
            technologies_dict[technologies_json[technology_name]].append(
                technology_name
            )

        elif technologies_json[technology_name] not in result["technologies"]:
            technologies_dict[technologies_json[technology_name]] = [technology_name]

    return result


def scrape_technologies_to_json(
    filename: str = f"{FILE_PATH}/db/technologies.json",
) -> None:
    html = get_html(url=TECHNOLOGIES_LINK)
    soup = bs(html, "lxml")
    tech_sel = soup.find("td", attrs={"class": "tech_sel"})
    links = tech_sel.find_all("a")
    categories = {}

    for link in links:
        href = link.get("href")
        name = link.text.strip()
        tech_html = get_html(url=href)
        technologies = parse_technologies_html(content=tech_html)
        categories[name] = technologies

    write_json(filename, data=categories)
