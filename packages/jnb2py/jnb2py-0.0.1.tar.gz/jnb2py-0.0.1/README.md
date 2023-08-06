# nb2py

*nb2py* is a Python library for converting Notebooks(`.ipynb`) into Python (`.py`) files.

## Quickstart

nb2py requires an installation of Python 3.10 or greater, as well as pip.

### Installation
pass

### Using nb2py in a Python Script

To convert a notebook, you'll need to do this.

```python
>> > from jnb2py import Converter
>> > file_path = "/path/to/the/notebook.ipynb"
>> > converter = Converter(file_path)
>> > output_file_name = "extract_code.py"
>> > output_path = "/path/to/the/output/destination"
>> > converter.convert_to_py(output_file_name, output_path)
```