To publish the project to the test environment of PyPI use:
```commandline
(venv)> python setup.py sdist
(venv)> python setup.py bdist_wheel --universal
(venv)> twine upload --config-file .\venv\pip.ini -r testpypi .\dist\* 
```

For publishing not into the piptest environment, replace the last line with:
```commandline
(venv)> twine upload --config-file .\venv\pip.ini .\dist\* 
```