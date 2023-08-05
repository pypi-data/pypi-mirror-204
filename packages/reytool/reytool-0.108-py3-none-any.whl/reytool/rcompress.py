# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-01-19 19:23:57
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's zip methods.
"""


from typing import List, Optional
from zipfile import ZipFile, is_zipfile, ZIP_DEFLATED
import os


def compress(obj_path: str, build_dir: Optional[str] = None, overwrite: bool = True) -> None:
    """
    Compress file or folder.

    Parameters
    ----------
    obj_path : File or folder path.
    build_dir : Build directory.
        - None : Work directory.
        - str : Use this value.

    overwrite : Whether to overwrite.
    """

    # Processing parameters.
    if build_dir == None:
        build_dir = os.getcwd()
    if overwrite:
        mode = "w"
    else:
        mode = "x"

    # Generate build path.
    basename = os.path.basename(obj_path)
    build_name = os.path.splitext(basename)[0]
    build_name += ".zip"
    build_path = os.path.join(build_dir, build_name)

    # Compress.
    with ZipFile(build_path, mode, ZIP_DEFLATED) as zip_file:
        zip_file.write(obj_path)
        is_dir = os.path.isdir(obj_path)

        ## Recursive compress.
        if is_dir:
            dirname = os.path.dirname(obj_path)
            dirname_len = len(dirname)
            dirs = os.walk(obj_path)
            for folder_name, sub_folders_name, files_name in dirs:
                for sub_folder_name in sub_folders_name:
                    sub_folder_path = os.path.join(folder_name, sub_folder_name)
                    zip_path = sub_folder_path[dirname_len:]
                    zip_file.write(sub_folder_path, zip_path)
                for file_name in files_name:
                    file_path = os.path.join(folder_name, file_name)
                    zip_path = file_path[dirname_len:]
                    zip_file.write(file_path, zip_path)

def decompress(obj_path: str, build_dir: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Decompress compressed object.

    Parameters
    ----------
    obj_path : Compressed object path.
    build_dir : Build directory.
        - None : Work directory.
        - str : Use this value.

    passwrod : Unzip Password.
        - None : No Unzip Password.
        - str : Use this value.
    """

    # Check object whether can be decompress.
    is_support = is_zipfile(obj_path)
    if not is_support:
        raise AssertionError("file format that cannot be decompressed")

    # Processing parameters.
    if build_dir == None:
        build_dir = os.getcwd()

    # Decompress.
    with ZipFile(obj_path) as zip_file:
        zip_file.extractall(build_dir, pwd=password)

def rzip(obj_path: str, build_dir: Optional[str] = None) -> None:
    """
    Automatic judge and compress or decompress object.

    Parameters
    ----------
    obj_path : File or folder or compressed object path.
    output_path : Build directory.
        - None : Work directory.
        - str : Use this value.
    """

    # Judge compress or decompress.
    is_support = is_zipfile(obj_path)

    # Execute.
    if is_support:
        decompress(obj_path, build_dir)
    else:
        compress(obj_path, build_dir)