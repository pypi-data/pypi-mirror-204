## DataModels Package
This file will explain how to test and upload your changes to this package. For an overview of the way the package works, please read the pypi-description.md.

Useful link on publishing: https://www.youtube.com/watch?v=GIF3LaRqgXo

### Developement
For development create a virtual env to test in and do developments in:

```bash
$ pip install virtualenv

$ virtualenv venv

$ source venv/bin/activate
```

to build your pymodule use these commands:
- This command will test you your py module will build.
```bash
$ python3 setup.py bdist_wheel
```

- This command will test you have met all the requirements needed for publishing a package
```bash
$ python3 setup.py sdist
```

### Testing
Install the requirements run this command in your virtual environment after
```bash
$ pip install -e ".[dev]"

$ pytest
```
this will install any dependencies from the current module needed to test and test them.

### Upload
To upload to the python package, please go into actions on github and into upload python package. 
Click run work flow and put in the version for the package desired. This will be in the format of 1.1.1. The latest version can be found here:
https://pypi.org/project/datamodelsFrontier/