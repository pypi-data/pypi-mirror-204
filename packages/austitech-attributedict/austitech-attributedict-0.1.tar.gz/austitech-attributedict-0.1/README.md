# AttributeDict
Python builtin dictionary extension that supports dot notation access. Trying to access a key that does not exist doesn't throw an exception

# Usage
```
from attributedict import AttributeDict


mydict = {"country": "Nigeria", "coords": [{"lat": 33567.6, "long": 37363.7}]}

mydict = AttributeDict(mydict)

coords = mydict.coords // [{"lat": 33567.6, "long": 37363.7}]

latitude = coords[0].lat // 33567.6

longitude = coords[0]["long"] // can also access it the traditional way
```

# Installation
Package can be installed from pypi using pip as below

```
pip install attributedict
```

Alternatively, clone the repo and install package from source as below:

```
git clone https://github.com/austitech/attributedict
cd attributedict
python3 setup.py sdist
```


### Thank You.