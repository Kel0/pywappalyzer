# Python wappalyzer  [![Build Status](https://cloud.drone.io/api/badges/Kel0/pywappalyzer/status.svg)](https://cloud.drone.io/Kel0/pywappalyzer) [![BCH compliance](https://bettercodehub.com/edge/badge/Kel0/pywappalyzer?branch=main)](https://bettercodehub.com/)
Modern and easy way to identify web technologies on site via Python

## Installation
- Install package from pypi
```commandline
pip install pywappalyzer
```
- Install & setup geckodriver
```shell
# if your platform is linux 
export GECKO_DRIVER_VERSION='v0.24.0'
wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz
chmod +x geckodriver
cp geckodriver /usr/local/bin/

# if your platform is windows pass this step
```

## Usage
Get technologies
```python
from pywappalyzer import Pywappalyzer


wappalyzer = Pywappalyzer()

data = wappalyzer.analyze(url="https://www.python.org/")
print(data)

>>> {'Web servers': ['Nginx'], 'Reverse proxies': ['Nginx'], 'Caching': ['Varnish'], 
>>>  'Analytics': ['Google Analytics'], 'JavaScript libraries': ['jQuery UI', 'Modernizr', 'jQuery']
```
Update technologies json list which use for identifying of technologies
```python
from pywappalyzer import Pywappalyzer


wappalyzer = Pywappalyzer()

wappalyzer.use_latest()  # call this method only once, for update the file
data = wappalyzer.analyze(url="https://www.python.org/")
print(data)

>>> {'Web servers': ['Nginx'], 'Reverse proxies': ['Nginx'], 'Caching': ['Varnish'], 
>>>  'Analytics': ['Google Analytics'], 'JavaScript libraries': ['jQuery UI', 'Modernizr', 'jQuery']}
```
Pywappalyzer uses selenium's `webdriver.Firefox` driver. For using `webdriver.Chrome` you need to write your own class
```python
from typing import Optional, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pywappalyzer import Site


class MySite(Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_html(
        self, url: Optional[str] = None, *, as_text: bool = False
    ) -> Union[bytes, str]:
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
        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            page_source = driver.page_source
            self.handle_js(driver)

        if as_text:
            return page_source
        return page_source.encode("utf-8")
```

# CONTRIBUTING
To contribute to the code, suppose you are working on Issue Ticket #34, you’ll need to create a new local branch named “feature/34”

git checkout -b "feature/34"

Now once you have made all changes,
```commandline
inv format (To format all the files according to Python standards)
```
```commandline
inv check (To check formatting once again)
```
```commandline
inv test (to run tests)
```
```commandline
git add .
```
```commandline
git commit -m "#34 <commit message>"
```
Example: ```git commit -m "#34 Add support for feature X"```
```commandline
git push --set-upstream origin feature/34
```
Now, your changes would have been pushed online to the new branch “feature/34”.

After this, you need to go to your branch online and create a Pull Request to merge the branch “feature/34” with “master”.

Once the Pull Request is approved after code review, you can merge the Pull Request. :-)

