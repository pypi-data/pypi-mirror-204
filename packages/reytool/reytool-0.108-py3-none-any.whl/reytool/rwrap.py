# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:12:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's decorators.
"""


from typing import Any, Tuple, Callable, Optional, Union, Literal, overload
from tqdm import tqdm as tqdm_tqdm
from threading import Thread
from functools import wraps as functools_wraps

from .rcommon import exc
from .rtext import print_frame
from .rdatetime import RDateTimeMark, now


def wrap_frame(decorator: Callable) -> Callable:
    """
    Decorative frame.

    Parameters
    ----------
    decorator : Decorator function.

    Retuens
    -------
    Decorator after decoration.

    Examples
    --------
    Decoration function method one.
    >>> @wrap_func
    >>> def func(): ...
    >>> func_ret = func(param_a, param_b, param_c=1, param_d=2)

    Decoration function method two.
    >>> def func(): ...
    >>> func_ret = wrap_func(func, param_a, param_b, param_c=1, param_d=2)

    Decoration function method three.
    >>> def func(): ...
    >>> func_ret = wrap_func(func, _execute=True)
    
    Decoration function method four.
    >>> def func(): ...
    >>> func = wrap_func(func)
    >>> func_ret = func(param_a, param_b, param_c=1, param_d=2)

    Decoration function method five.
    >>> def func(): ...
    >>> func = wrap_func(func, param_a, param_c=1, _execute=False)
    >>> func_ret = func(param_b, param_d=2)
    """

    # Decorate Decorator.
    @functools_wraps(decorator)
    def wrap(func: Callable, *args: Any, _execute: Optional[bool] = None, **kwargs: Any) -> Union[Callable, Any]:
        """
        Decorative shell.

        Parameters
        ----------
        _execute : Whether execute function, otherwise decorate function.
            - None : When parameter 'args' or 'kwargs' have values, then True, otherwise False.
            - bool : Use this value.
        
        Returns
        -------
        Function after decoration or return of function.
        """

        # Handle parameters.
        if _execute == None:
            if args != () or kwargs != {}:
                _execute = True
            else:
                _execute = False

        # Direct execution.
        if _execute:
            func_ret = decorator(func, *args, **kwargs)
            return func_ret

        # Decorate function.
        @functools_wraps(func)
        def wrap_sub(*_args: object, **_kwargs: object) -> object:
            """
            Decorative sub shell.
            """

            # Decorate function.
            func_ret = decorator(func, *args, *_args, **kwargs, **_kwargs)

            return func_ret

        return wrap_sub

    return wrap

def wraps(*wrap_funcs: Callable) -> Callable:
    """
    Batch decorate.

    Parameters
    ----------
    wrap_funcs : Decorator function.

    Retuens
    -------
    Function after decoration.

    Examples
    --------
    Decoration function.
    >>> @wraps(print_funtime, state_thread)
    >>> def func(): ...
    >>> func_ret = func()

        Same up and down

    >>> @print_funtime
    >>> @state_thread
    >>> def func(): ...
    >>> func_ret = func()

        Same up and down

    >>> def func(): ...
    >>> func = print_funtime(func)
    >>> func = state_thread(func)
    >>> func_ret = func()
    """

    # Sequential decorate.
    def func(): ...
    for wrap_func in wrap_funcs:

        ## One shell.
        @functools_wraps(func)
        def wrap(func: Callable) -> Callable:
            """
            Decorative shell
            """

            ## Two shell.
            @functools_wraps(func)
            def wrap_sub(*args: object, **kwargs: object) -> object:
                """
                Decorative sub shell
                """

                # Decorate.
                func_ret = wrap_func(func, *args, _execute=True, **kwargs)

                return func_ret

            return wrap_sub

        func = wrap

    return wrap

@overload
def runtime(func: Callable, *args: Any, _ret_report: bool = False, **kwargs: Any) -> Union[Any, Tuple[Any, str]]: ...

@overload
def runtime(_ret_report: Literal[False]) -> Any: ...

@overload
def runtime(_ret_report: Literal[True]) -> Union[Any, Tuple[Any, str]]: ...

@wrap_frame
def runtime(func: Callable, *args: Any, _ret_report: bool = False, **kwargs: Any) -> Union[Any, Tuple[Any, str]]:
    """
    Print or return runtime report of the function.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position parameter of input parameter decorated function.
    _ret_report : Whether return report, otherwise print report.
    kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Function run result or runtime report.
    """

    # Run function and marking time.
    rtm = RDateTimeMark()
    func_ret = func(*args, **kwargs)
    rtm.mark()

    # Generate report.
    runtime = rtm.record[-1]["interval_timestamp"] / 1000
    report = "Start: %s -> Spend: %ss -> End: %s" % (
        rtm.record[0]["datetime_str"],
        runtime,
        rtm.record[1]["datetime_str"]
    )
    title = func.__name__

    # Return report.
    if _ret_report:
        return func_ret, report

    # Print report.
    print_frame(report, title=title)

    return func_ret

@overload
def start_thread(func: Callable, *args: Any, _daemon: bool = True, **kwargs: Any) -> Thread: ...

@wrap_frame
def start_thread(func: Callable, *args: Any, _daemon: bool = True, **kwargs: Any) -> Thread:
    """
    Function start in thread.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position parameter of input parameter decorated function.
    _daemon : Whether it is a daemon thread.
    kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Thread object.
    """

    # Handle parameters.
    thread_name = "%s_%d" % (func.__name__, now("timestamp"))

    # Create thread.
    thread = Thread(target=func, name=thread_name, args=args, kwargs=kwargs)
    thread.daemon = _daemon

    # Start thread.
    thread.start()

    return thread

@overload
def try_exc(func: Callable, *args: Any, **kwargs: Any) -> Optional[Any]: ...

@wrap_frame
def try_exc(func: Callable, *args: Any, **kwargs: Any) -> Optional[Any]:
    """
    Execute function with 'try' syntax and print error information.

    Parameters
    ----------
    func : Function to be decorated.
    args : Position parameter of input parameter decorated function.
    kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Function run result or no return.
    """

    # Run function.
    try:
        func_ret = func(*args, **kwargs)

    # Print error information.
    except:
        func_name = func.__name__
        exc(func_name)

    # Return function result.
    else:
        return func_ret

@overload
def update_tqdm(
    func: Callable,
    tqdm: tqdm_tqdm,
    *args: Any,
    _desc: Optional[str] = None,
    _step: Union[int, float] = 1,
    **kwargs: Any
) -> Any: ...

@wrap_frame
def update_tqdm(
    func: Callable,
    tqdm: tqdm_tqdm,
    *args: Any,
    _desc: Optional[str] = None,
    _step: Union[int, float] = 1,
    **kwargs: Any
) -> Any:
    """
    Update progress bar tqdm object of tqdm package.

    Parameters
    ----------
    func : Function to be decorated.
    tqdm : Progress bar tqdm object.
    args : Position parameter of input parameter decorated function.
    _desc : Progress bar description.
        - None : no description.
        - str : Add description.

    _step : Progress bar step size.
        - When greater than 0, then forward.
        - When less than 0, then backward.

    kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Function run result or no return.
    """

    # Set description.
    if _desc != None:
        tqdm.set_description(_desc)

    # Run function.
    func_ret = func(*args, **kwargs)

    # Update progress bar.
    tqdm.update(_step)

    return func_ret