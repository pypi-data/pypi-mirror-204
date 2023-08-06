import json
from typing import AnyStr, Dict, Any, List

from jnb2py.models import Cell
from jnb2py.utils import write_to_a_file

NEW_LINE_CHARACTER = "\n"


class Converter:
    """
    A class to Convert ipynb notebook to python file

    :param nb_file_path: file path of the notebook file.
    :type nb_file_path: str
    """

    def __init__(self, nb_file_path: str) -> None:
        self.nb_file_path: str = nb_file_path

    def convert_to_py(self, file_name: str, dest_path: str) -> None:
        """
        Converts the ipynb notebook to py file

        :param file_name: output python file name
        :type file_name: str
        :param dest_path: destination path of the output file
        :type dest_path: str
        :return: None
        """
        try:
            # all the cells from the notebook
            cells = self._parse_notebook().get("cells")

            # convert all the cells into Cell object
            all_cells: List[Cell] = [Cell(**cell) for cell in cells]

            code = ""
            for cell in all_cells:
                if cell.cell_type == "code":
                    for source_line in cell.source:
                        if not source_line.endswith(NEW_LINE_CHARACTER):
                            code += source_line + NEW_LINE_CHARACTER
                        else:
                            code += source_line

            write_to_a_file(content=code, file_name=file_name, dest_path=dest_path)

        except Exception as e:
            print(str(e))

    def _parse_notebook(self) -> Dict[str, Any]:
        """
         As we can see that the structure of the .ipynb file
        is like JSON file, we can read convert this to a
        Python dictionary.

        :return: dictionary version of the notebook
        :rtype: dict
        """
        try:
            # getting the notebook data, which is in JSON format
            notebook_data: AnyStr = self._get_data_from_notebook()

            # parse JSON string to dictionary
            notebook_dict: Dict[str, Any] = json.loads(notebook_data)

            return notebook_dict

        except Exception as e:
            print(str(e))

    def _get_data_from_notebook(self) -> AnyStr:
        """
        Read the notebook from the specified file_path

        :return: string of the data
        :rtype: AnyStr
        """

        try:
            with open(self.nb_file_path, "r") as f_obj:
                data: AnyStr = f_obj.read()
            return data

        except Exception as e:
            print(str(e))
