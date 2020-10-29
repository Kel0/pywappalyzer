# pywappalyzer  [![Build Status](https://cloud.drone.io/api/badges/Kel0/pywappalyzer/status.svg)](https://cloud.drone.io/Kel0/pywappalyzer) [![BCH compliance](https://bettercodehub.com/edge/badge/Kel0/pywappalyzer?branch=main)](https://bettercodehub.com/)

## Installation
```commandline
pip install pywappalyzer
```

## Usage
Get technologies
```python
from pywappalyzer import Pywappalyzer


wappalyzer = Pywappalyzer()

data = wappalyzer.analyze(url="https://google.com")
print(data)
```
Update technologies json list which use for identifying of technologies
```python
from pywappalyzer import Pywappalyzer


wappalyzer = Pywappalyzer()

wappalyzer.use_latest()  # run only once for update the file
data = wappalyzer.analyze(url="https://google.com")
print(data)
```

