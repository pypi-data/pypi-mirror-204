# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey"s basic methods.
"""


from typing import Any, List, Tuple, Iterable, Callable, Type, Literal, Optional, Union
from warnings import warn as warnings_warn
from varname import argname


def warn(*warn_infos: Any, warn_type: Type[BaseException] = UserWarning, stacklevel: int = 3) -> None:
    """
    Throw warning.

    Parameters
    ----------
    warn_info : Warn informations.
    warn_type : Warn type.
    stacklevel : Warning code location, number of recursions up the code level.
    """

    # Handle parameters.    
    if warn_infos == ():
        warn_infos = "Warning!"
    elif len(warn_infos) == 1:
        if type(warn_infos[0]) == str:
            warn_infos = warn_infos[0]
        else:
            warn_infos = str(warn_infos[0])
    else:
        warn_infos = str(warn_infos)

    # Throw warning.
    warnings_warn(warn_infos, warn_type, stacklevel)

def check_target(value: Any, *targets: Union[Any, Literal["_iterable"]], check_element: bool = False) -> None:
    """
    Check the content or type of the value, when check fail, then throw error.

    Parameters
    ---------
    value : Check object.
    targets : Correct target, can be type.
        - Any : Check whether it is the target.
        - Literal['_iterable'] : Check whether it can be iterable.

    check_element : Whether check element in value.
    """

    # Handle parameters.
    if check_element:
        values = value
    else:
        values = [value]

    # Check.
    for element in values:

        ## Check sub elements.
        if "_iterable" in targets and is_iterable(element):
            continue

        ## Right tragets.
        if type(element) in targets:
            continue
        targets_id = [id(target) for target in targets]
        if id(element) in targets_id:
            continue

        ## Throw error.
        var_name = get_name(value)
        if var_name != None:
            var_name = " '%s'" % var_name
        else:
            var_name = ""
        correct_targets_str = ", ".join([repr(target) for target in targets])
        if check_element:
            raise ValueError(
                "parameter%s the elements content or type must in [%s], now: %s" % (
                    var_name,
                    correct_targets_str,
                    repr(value)
                )
            )
        else:
            raise ValueError(
                "parameter%s the content or type must in [%s], now: %s" % (
                    var_name,
                    correct_targets_str,
                    repr(value)
                )
            )

def check_least_one(*values: Any) -> None:
    """
    Check that at least one of multiple values is not None, when check fail, then throw error.

    Parameters
    ----------
    values : Check values.
    """

    # Check.
    for value in values:
        if value != None:
            return

    # Throw error.
    vars_name = get_name(values)
    if vars_name != None:
        vars_name_de_dup = list(set(vars_name))
        vars_name_de_dup.sort(key=vars_name.index)
        vars_name_str = " " + " and ".join(["'%s'" % var_name for var_name in vars_name_de_dup])
    else:
        vars_name_str = ""
    raise ValueError("at least one of parameters%s is not None" % vars_name_str)

def check_most_one(*values: Any) -> None:
    """
    Check that at most one of multiple values is not None, when check fail, then throw error.

    Parameters
    ----------
    values : Check values.
    """

    # Check.
    none_count = 0
    for value in values:
        if value != None:
            none_count += 1

    # Throw error.
    if none_count > 1:
        vars_name = get_name(values)
        if vars_name != None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join(["'%s'" % var_name for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError("at most one of parameters%s is not None" % vars_name_str)

def is_iterable(obj: Any, exclude_types: Iterable[Type] = [str, bytes]) -> bool:
    """
    Judge whether it is iterable.

    Parameters
    ----------
    obj : Judge object.
    exclude_types : Non iterative types.

    Returns
    -------
    Judgment result.
    """

    # Exclude types.
    if type(obj) in exclude_types:
        return False

    # Judge.
    try:
        obj_dir = obj.__dir__()
    except TypeError:
        return False
    if "__iter__" in obj_dir:
        return True
    else:
        return False

def is_table(obj: Any, check_fields: bool = True) -> bool:
    """
    Judge whether it is List[Dict] table format and keys and keys sort of the Dict are the same.

    Parameters
    ----------
    obj : Judge object.
    check_fields : Do you want to check the keys and keys sort of the Dict are the same.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    if type(obj) != list:
        return False
    for element in obj:
        if type(element) != dict:
            return False

    ## Check fields of table.
    if check_fields:
        keys_strs = [
            ":".join([str(key) for key in element.keys()])
            for element in obj
        ]
        keys_strs_only = set(keys_strs)
        if len(keys_strs_only) != 1:
            return False

    return True

def is_number_str(text: str) -> bool:
    """
    Judge whether it is number string.

    Parameters
    ----------
    text : Judge text.
    return_value : Whether return value.

    Returns
    -------
    Judgment result.
    """

    # Judge.
    try:
        if "." in text:
            number = float(text)
        else:
            number = int(text)
    except ValueError:
        return False

    return True

def get_first_notnull(
    *values: Any,
    default: Optional[Union[Any, Literal["error"]]] = None,
    null_values: List = [None]) -> Any:
    """
    Get the first value that is not null.

    Parameters
    ----------
    values : Check values.
    default : When all are null, then return this is value, or throw error.
        - Any : Return this is value.
        - Literal['error'] : Throw error.

    null_values : Range of null values.

    Returns
    -------
    Return first not null value, when all are null, then return default value.
    """

    # Get value.
    for value in values:
        if value not in null_values:
            return value

    # Throw error.
    if default == "error":
        vars_name = get_name(values)
        if vars_name != None:
            vars_name_de_dup = list(set(vars_name))
            vars_name_de_dup.sort(key=vars_name.index)
            vars_name_str = " " + " and ".join(["'%s'" % var_name for var_name in vars_name_de_dup])
        else:
            vars_name_str = ""
        raise ValueError("at least one of parameters%s is not None" % vars_name_str)

    return default

def ins(obj: Any, *arrays: Iterable) -> bool:
    """
    Judge whether the object is in multiple array.

    Parameters
    ----------
    obj : Judge object.
    arrays : Array.

    Returns
    -------
    Judge result.
    """

    # Judge.
    for array in arrays:
        if obj in array:
            return True

    return False

def mutual_in(*arrays: Iterable) -> bool:
    """
    Whether the same element exists in multiple array.

    Parameters
    ----------
    arrays : Array.

    Returns
    -------
    Judge result.
    """

    # Handle parameters.
    arrays = list(arrays)

    # Judge.
    for n, array in enumerate(arrays):
        for after_array in arrays[n+1:]:
            for element in array:
                if ins(element, after_array):
                    return True

    return False

def to_type(obj: Any, to_type: Type, method: Optional[Callable] = None) -> Any:
    """
    Convert object type.

    Parameters
    ----------
    obj : Convert object.
    to_type : Target type.
    method : Convert method.
        - None : Use value of parameter 'to_type'.
        - Callable : Use this method.

    Returns
    -------
    Converted object.
    """

    # Judge type.
    if type(obj) == to_type:
        return obj

    # Convert type.
    if method != None:
        return method(obj)
    else:
        return to_type(obj)

def get_name(obj: Any, frame: int = 2) -> Optional[Union[str, Tuple[str, ...]]]:
    """
    Get object name.

    Parameters
    ----------
    obj : Object.
    frame : Number of code to upper level.

    Returns
    -------
    Object name or None.
    """

    # Get name using built in method.
    try:
        name = obj.__name__
    except AttributeError:

        # Get name using module method.
        name = "obj"
        try:
            for _frame in range(1, frame + 1):
                name = argname(name, frame=_frame)
            if type(name) != str:
                if "".join(name) == "":
                    name = None
        except:
            name = None

    return name