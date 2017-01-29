# Elformat
Tool for formatting your elisp source code

## Usage
Start tests:
```bash
python3 -m unittest -v test
```
or
```bash
python3 -m unittest discover
```
Test project style:
```bash
pylint src
```

### Generate documentation
Add new modules to autodocumentation sources:
```bash
sphinx-apidoc -o docs/source src
```

Generate html:
```bash
cd docs
make html
```
