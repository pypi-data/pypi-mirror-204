# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 13:11:09
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's common methods.
"""


from typing import List, Tuple, Literal, Optional, Union
import os
import re
import time
import random
from traceback import format_exc

from . import roption
from .rtext import rprint


def exc(title: str = "Error", report: bool = True) -> str:
    """
    Print and return error messages, must used in 'except' syntax.

    Parameters
    ----------
    title : Print title.
    report : Whether print error messages.

    Returns
    -------
    Error messages.
    """

    # Get error information.
    error = format_exc()
    error = error.strip()

    # Report.
    if report:
        rprint(error, title=title, frame=roption.print_default_frame_half)

    return error

def digits(number: Union[int, float]) -> Tuple[int, int]:
    """
    Judge the number of integer digits and deciaml digits.

    Parameters
    ----------
    number : Number to judge.

    Returns
    -------
    Integer digits and deciaml digits.
    """

    # Handle parameters.
    number_str = str(number)

    # Get digits.
    if "." in number_str:
        integer_str, decimal_str = number_str.split(".")
        integer_digits = len(integer_str)
        deciaml_digits = len(decimal_str)
    else:
        integer_digits = len(number_str)
        deciaml_digits = 0

    return integer_digits, deciaml_digits

def randn(*thresholds: Union[int, float], precision: Optional[int] = None) -> Union[int, float]:
    """
    Get random number.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When length is 0, then low and high thresholds is 0 and 10.
        - When length is 1, then low and high thresholds is 0 and thresholds[0].
        - When length is 2, then low and high thresholds is thresholds[0] and thresholds[1].

    precision : Precision of random range, that is maximum decimal digits of return value.
        - None : Set to Maximum decimal digits of element of parameter 'thresholds'.
        - int : Set to this value.

    Returns
    -------
    Random number.
        - When parameters 'precision' is 0, then return int.
        - When parameters 'precision' is greater than 0, then return float.
    """

    # Handle parameters.
    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        threshold_low = 0
        threshold_high = 10
    elif thresholds_len == 1:
        threshold_low = 0
        threshold_high = thresholds[0]
    elif thresholds_len == 2:
        threshold_low = thresholds[0]
        threshold_high = thresholds[1]
    else:
        raise ValueError("number of parameter 'thresholds' must is 0 or 1 or 2")
    if precision == None:
        threshold_low_desimal_digits = digits(threshold_low)[1]
        threshold_high_desimal_digits = digits(threshold_high)[1]
        desimal_digits_max = max(threshold_low_desimal_digits, threshold_high_desimal_digits)
        precision = desimal_digits_max

    # Get random number.
    magnifier = 10 ** precision
    threshold_low *= magnifier
    threshold_high *= magnifier
    number = random.randint(threshold_low, threshold_high)
    number = number / magnifier
    if precision == 0:
        number = int(number)

    return number

def sleep(*thresholds: Union[int, float], precision: Optional[int] = None) -> Union[int, float]:
    """
    Sleep random seconds.

    Parameters
    ----------
    thresholds : Low and high thresholds of random range, range contains thresholds.
        - When length is 0, then low and high thresholds is 0 and 10.
        - When length is 1, then sleep this value.
        - When length is 2, then low and high thresholds is thresholds[0] and thresholds[1].
    
    precision : Precision of random range, that is maximum decimal digits of sleep seconds.
        - None : Set to Maximum decimal digits of element of parameter 'thresholds'.
        - int : Set to this value.
    
    Returns
    -------
    Random seconds.
        - When parameters 'precision' is 0, then return int.
        - When parameters 'precision' is greater than 0, then return float.
    """

    # Handle parameters.
    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        second = randn(0, 10, precision=precision)
    elif thresholds_len == 1:
        second = thresholds[0]
    elif thresholds_len == 2:
        second = randn(thresholds[0], thresholds[1], precision=precision)
    else:
        raise ValueError("number of parameter 'thresholds' must is 0 or 1 or 2")

    # Sleep.
    time.sleep(second)

    return second

def get_paths(path: Optional[str] = None, target: Literal["all", "file", "folder"] = "all", recursion: bool = True) -> List:
    """
    Get the path of files and folders in the path.

    Parameters
    ----------
    path : When None, then work path.
    target : Target data.
        - "all" : Return file and folder path.
        - "file : Return file path.
        - "folder" : Return folder path.

    recursion : Is recursion directory.

    Returns
    -------
    String is path.
    """

    # Handle parameters.
    if path == None:
        path = ""
    path = os.path.abspath(path)

    # Get paths.
    paths = []

    ## Recursive.
    if recursion:
        obj_walk = os.walk(path)
        if target == "all":
            targets_path = [
                os.path.join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name + folders_name
            ]
            paths.extend(targets_path)
        elif target == "file":
            targets_path = [
                os.path.join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name
            ]
            paths.extend(targets_path)
        elif target in ["all", "folder"]:
            targets_path = [
                os.path.join(path, folder_name)
                for path, folders_name, files_name in obj_walk
                for folder_name in folders_name
            ]
            paths.extend(targets_path)

    ## Non recursive.
    else:
        names = os.listdir(path)
        if target == "all":
            for name in names:
                target_path = os.path.join(path, name)
                paths.append(target_path)
        elif target == "file":
            for name in names:
                target_path = os.path.join(path, name)
                is_file = os.path.isfile(target_path)
                if is_file:
                    paths.append(target_path)
        elif target == "folder":
            for name in names:
                target_path = os.path.join(path, name)
                is_dir = os.path.isdir(target_path)
                if is_dir:
                    paths.append(target_path)

    return paths

map_digit = {
    "0": "零",
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
}

map_digits = {
    0: "",
    1: "十",
    2: "百",
    3: "千",
    4: "万",
    5: "十",
    6: "百",
    7: "千",
    8: "亿",
    9: "十",
    10: "百",
    11: "千",
    12: "万",
    13: "十",
    14: "百",
    15: "千",
    16: "兆"
}

def n_to_ch(number: int) -> str:
    """
    Convert number to chinese number.

    Parameters
    ----------
    number : Number to convert.

    Returns
    -------
    Chinese number.
    """

    # Processing parameters.
    number = str(number)

    # Replace digit.
    for digit, digit_ch in map_digit.items():
        number = number.replace(digit, digit_ch)

    # Add digits.
    number_list = []
    for index, digit_ch in enumerate(number[::-1]):
        digits_ch = map_digits[index]
        number_list.insert(0, digits_ch)
        number_list.insert(0, digit_ch)
    number = "".join(number_list)

    # Delete redundant content.
    pattern = "(?<=零)[^万亿兆]"
    number = re.sub(pattern, "", number)
    pattern = "零+"
    number = re.sub(pattern, "零", number)
    pattern = "零(?=[万亿兆])"
    number = re.sub(pattern, "", number)
    if number[0:2] == "一十":
        number = number[1:]
    if number[-1:] == "零":
        number = number[:-1]

    return number