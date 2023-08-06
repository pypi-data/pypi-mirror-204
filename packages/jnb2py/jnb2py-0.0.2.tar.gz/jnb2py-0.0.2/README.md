# jnb2py

*jnb2py* is a Python library for converting Notebooks(`.ipynb`) into Python (`.py`) files.

## Quickstart

jnb2py requires an installation of Python 3.10 or greater, as well as pip.

### Installation
jnb2py requires an installation of Python 3.10 or greater, as well as pip. (Pip is typically bundled with Python installations.)

To install from PyPI with pip:
```bash
pip install jnb2py
```

### Using nb2py in a Python Script

To convert a notebook, you'll need to do this.

```python
>>> from jnb2py import Converter
>>> file_path = "/path/to/the/notebook.ipynb"
>>> converter = Converter(file_path)
>>> output_file_name = "extract_code.py"
>>> output_path = "/path/to/the/output/destination"
>>> converter.convert_to_py(output_file_name, output_path)
```
