from jnb2py.nbconverter import Converter
import os


def test_convert_to_py():
    file_name = "test_output.py"
    output_path = "examples/"
    converter = Converter("examples/notebooks/temp.ipynb")
    converter.convert_to_py(file_name=file_name, dest_path=output_path)

    with open(os.path.join(output_path, file_name), "r") as f_obj:
        data = f_obj.readlines()

    print(data)
    assert data == ['import math as mp\n', "print('Hello, world')\n"]