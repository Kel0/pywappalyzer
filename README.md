# Python wappalyzer  [![Build Status](https://cloud.drone.io/api/badges/Kel0/pywappalyzer/status.svg)](https://cloud.drone.io/Kel0/pywappalyzer) [![BCH compliance](https://bettercodehub.com/edge/badge/Kel0/pywappalyzer?branch=main)](https://bettercodehub.com/)
Easy identify web technologies on site via Python

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

wappalyzer.use_latest()  # call this method only once, for update the file
data = wappalyzer.analyze(url="https://google.com")
print(data)
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

