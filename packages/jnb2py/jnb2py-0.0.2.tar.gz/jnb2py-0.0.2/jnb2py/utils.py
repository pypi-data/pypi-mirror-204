import os


def write_to_a_file(content: str, file_name: str, dest_path: str) -> None:
    """
    Writing to a file.

    :param content: content to write
    :type content: str
    :param file_name: output file name
    :type file_name: str
    :param dest_path: output file's path
    :type dest_path: str
    :return: None
    """
    with open(os.path.join(dest_path, file_name), "w") as f_obj:
        f_obj.write(content)
