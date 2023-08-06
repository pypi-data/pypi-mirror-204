import traceback
import re
from .Typing import Callable, Any, Union
import functools
import threading
import inspect
from .Functions import areoneof, isoneof, isoneof_strict, isoftype
from .Exceptions import *


def validate(func: Callable) -> Callable:
    """A decorator that validates the annotations and types of the arguments and return value of a function.

        * 'None' is allowed as default value for everything
        * Because of their use in classes, the generally accepted keywords 'self' and 'cls' are not validated to not break intellisense when using 'Any'

    Args:
        func (Callable): The function to be decorated.

    Raises:
        TypeError: if the decorated object is nto a Callable
        EmptyAnnotationException: If an argument is not annotated.
        InvalidDefaultValueException: If an argument's default value is not of the annotated type.
        ValidationException: If an argument's value is not of the expected type.
        InvalidReturnValueException: If the return value is not of the expected type.

    Returns:
        Callable: A wrapper function that performs the validation and calls the original function.
    """
    if not isinstance(func, Callable):
        raise TypeError("The validate decorator must only decorate a function")
    func_name = f"{func.__module__}.{func.__qualname__}"
    # get the signature of the function
    signature = inspect.signature(func)
    for arg_name, arg_param in signature.parameters.items():
        if arg_name not in {"self", "cls"}:
            arg_type = arg_param.annotation
            # check if an annotation is missing
            if arg_type == inspect.Parameter.empty:
                raise EmptyAnnotationException(
                    f"In {func_name}, argument '{arg_name}' is not annotated")

        # check if the argument has a default value
        default_value = signature.parameters[arg_name].default
        if default_value != inspect.Parameter.empty:
            # allow everything to be set to None as default
            if default_value is None:
                continue
            # if it does, check the type of the default value
            if not isoftype(default_value, arg_type):
                raise InvalidDefaultValueException(
                    f"In {func_name}, argument '{arg_name}'s default value is annotated as {arg_type} but got '{default_value}' which is {type(default_value)}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function for the type validating - will run on each call independently
        """
        # check all arguments
        bound = signature.bind(*args, **kwargs)
        for variable_name, variable_value in bound.arguments.items():
            annotated_type = signature.parameters[variable_name].annotation
            expected_type = func.__annotations__[variable_name]
            if not isoftype(variable_value, expected_type):
                raise ValidationException(
                    f"In {func_name}, argument '{variable_name}' is annotated as {annotated_type} but got '{variable_value}' which is {type(variable_value)}")

        # call the function
        result = func(*args, **kwargs)

        # check the return type
        return_type = type(None) if ("inspect._empty" in str(signature.return_annotation)
                                     or signature.return_annotation is None) else signature.return_annotation
        if not isoftype(result, return_type):
            raise InvalidReturnValueException(
                f"In function {func_name}, the return type is annotated as {return_type} but got '{result}' which is {type(result)}")
        return result
    return wrapper


# __validation_set = set()
# __validation_instantiation_rule = dict()


# def __validate_type(func: Callable, v: Any, T: type, validation_func: Callable[[Any], bool] = isoftype, msg: str = None) -> None:
#     if not validation_func(v, T):
#         raise ValidationTypeError(
#             msg or f"In {func.__module__}.{func.__qualname__}(...)\nThe argument is: '{ v.__qualname__ if hasattr(v, '__qualname__') else v}'\nIt has the type of '{type(v)}'\nIt is marked as type(s): '{T}'")


# def __validate_condition(func: Callable, v: Any, constraint: Callable[[Any], bool], msg: str = None) -> None:
#     if not constraint(v):
#         raise ValidationValueError(
#             msg or f"In {func.__module__}.{func.__qualname__}(...)\nThe argument '{str(v)}' has failed provided constraint\nConstraint in {constraint.__module__}.{constraint.__qualname__}")


# def __validate_arg(func: Callable, curr_arg: Any, curr_inner_arg: Any) -> None:
#     if isoneof(curr_arg, [list, tuple]):
#         # multiple type only:
#         if areoneof(curr_arg, [type]):
#             __validate_type(func, curr_inner_arg, curr_arg, isoneof)

#         else:  # maybe with condition:
#             class_type, constraint = curr_arg[0], curr_arg[1]

#             # Type validation
#             if isoneof(class_type, [list, tuple]):
#                 __validate_type(func, curr_inner_arg, class_type, isoneof)
#             else:
#                 __validate_type(func, curr_inner_arg, class_type, isinstance)

#             # constraints validation
#             if constraint is not None:
#                 message = curr_arg[2] if len(curr_arg) > 2 else None
#                 __validate_condition(func, curr_inner_arg, constraint, message)
#     else:
#         __validate_type(func, curr_inner_arg, curr_arg)


# def validate_explicit(*args, return_type=None, can_instantiate_multiple_times: bool = False) -> Callable:
#     """validate decorator

#         Is passed types of variables to perform type checking over\n
#         The arguments must be passed in the same order\n

#     for each parameter respectively you can choose one of four options:\n
#         1. None - to skip\n
#         2. Type - a type to check \n
#         3. Sequence of Type to check if the type is contained in the sequence\n
#         4. Sequence that contains three arguments:\n
#             4.1 a Type or Sequence[Type]\n
#             4.2 a function to call on argument\n
#             4.3 a str to display in a ValueError iff the condition from 4.2 fails\n
#     In addition you can use keyword 'return_type' for the returned value same as specified in 1,2,3
#     """
#     from .Exceptions import ValidationDuplicationError, ValidationTypeError, ValidationValueError, ValidationReturnTypeError

#     def deco(func: Callable) -> Callable:
#         if not isinstance(func, Callable):
#             raise ValueError("validate decorator must decorate a callable")
#         global __validation_set, __validation_instantiation_rule
#         func_id = f"{func.__module__}.{func.__qualname__}"

#         if func_id not in __validation_instantiation_rule:
#             __validation_instantiation_rule[func_id] = can_instantiate_multiple_times
#         assert can_instantiate_multiple_times == __validation_instantiation_rule[
#             func_id], "can't change instantiation status on runtime"

#         if func_id not in __validation_set:
#             __validation_set.add(func_id)
#         else:
#             if not __validation_instantiation_rule[func_id]:
#                 raise ValidationDuplicationError(
#                     "validate decorator is being used on two functions in the same module with the same name\nmaybe use @overload instead")

#         @ functools.wraps(func)
#         def wrapper(*inner_args, **inner_kwargs) -> Any:
#             for i in range(min(len(args), len(inner_args))):
#                 if args[i] is not None:
#                     __validate_arg(func, args[i], inner_args[i])
#             res = func(*inner_args, **inner_kwargs)
#             if return_type is not None:
#                 msg = f"In {func.__module__}.{func.__qualname__}(...)\nThe returned value is: '{ res.__qualname__ if hasattr(res, '__qualname__') else res}'\nIt has the type of '{type(res)}'\nIt is marked as type(s): '{return_type}'"
#                 __validate_type(func, res, return_type, msg=msg)
#             return res
#         return wrapper
#     return deco


@validate
def NotImplemented(func: Callable) -> Callable:
    """decorator to mark function as not implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        raise NotImplementedError(
            f"As marked by the developer {func.__module__}.{func.__qualname__} is not implemented yet..")
    return wrapper


@validate
def PartiallyImplemented(func: Callable) -> Callable:
    """decorator to mark function as not fully implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    from .Colors import warning

    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        warning(
            f"As marked by the developer, {func.__module__}.{func.__qualname__} may not be fully implemented and might not work properly")
        return func(*args, **kwargs)
    return wrapper


@validate
def memo(func: Callable) -> Callable:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: dict[tuple, Any] = {}

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return cache[(args, *kwargs.items())]
    return wrapper


__overload_dict: dict[str, dict[tuple, Callable]] = dict()


def overload(*types) -> Callable:
    """decorator for overloading functions\n
    Usage\n-------\n
    @overload(str,str)\n
    def print_info(name,color):
        ...\n\n
    @overload(str,[int,float]))\n
    def print_info(name,age):
        ...\n\n

    * use None to skip argument
    * use no arguments to mark as default function
    * you should overload in decreasing order of specificity! e.g @overload(int) should appear in the code before @overload(Any)

    \n\n\n
    \nRaises:
        OverloadDuplication: if a functions is overloaded twice (or more) with same argument types
        OverloadNotFound: if an overloaded function is called with types that has no variant of the function

    \nNotice:
        The function's __doc__ will hold the value of the last variant only
    """
    # make sure to use unique global dictionary
    if len(types) == 1 and type(types[0]).__name__ == "function":
        raise ValueError("can't create an overload without defining types")
    global __overload_dict
    # allow input of both tuples and lists for flexibly
    if len(types) > 0:
        types = list(types)
        for i, maybe_list_of_types in enumerate(types):
            if isoneof(maybe_list_of_types, [list, tuple]):
                types[i] = tuple(sorted(list(maybe_list_of_types),
                                        key=lambda sub_type: sub_type.__name__))
        types = tuple(types)

    def deco(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise TypeError("overload decorator must be used on a callable")

        # assign current overload to overload dictionary
        name = f"{func.__module__}.{func.__qualname__}"

        if name not in __overload_dict:
            __overload_dict[name] = dict()

        if types in __overload_dict[name]:
            # raise if current overload already exists for current function
            raise OverloadDuplication(
                f"{name} has duplicate overloading for type(s): {types}")

        __overload_dict[name][types] = func

        @ functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            default_func = None
            # select correct overload
            for variable_types, curr_func in __overload_dict[f"{func.__module__}.{func.__qualname__}"].items():
                if len(variable_types) == 0:
                    if default_func is None:
                        default_func = curr_func
                        continue
                    else:
                        # will not reach here because of duplicate overloading so this is redundant
                        raise ValueError("Can't have two default functions")

                if len(variable_types) != len(args):
                    continue

                for i, variable_type in enumerate(variable_types):
                    if variable_type is not None:
                        if isoneof(variable_type, [list, tuple]):
                            if not isoneof_strict(args[i], variable_type):
                                break
                        else:
                            if not isoftype(args[i], variable_type):
                                break
                else:
                    return curr_func(*args, **kwargs)

            if default_func is not None:
                return default_func(*args, **kwargs)
            # or raise exception if no overload exists for current arguments
            raise OverloadNotFound(
                f"function {func.__module__}.{func.__qualname__} is not overloaded with {[type(v) for v in args]}")

        return wrapper
    return deco


@validate
def abstractmethod(func: Callable) -> Callable:
    """A decorator to mark a function to be 'pure virtual' / 'abstract'

    Args:
        func (Callable): the function to mark

    Raises:
        NotImplementedError: the error that will rise when the marked function will be called if not overridden in a derived class
    """
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"{func.__module__}.{func.__qualname__} MUST be overridden in a child class")
    return wrapper


# __virtualization_tables = dict()


# @NotImplemented
# def virtual(func: Callable) -> Callable:
#     def wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper


# @NotImplemented
# def override(func: Callable) -> Callable:
#     def wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper


# @ PartiallyImplemented
# @validate
# def deprecate(obj:  Callable) -> Callable:
#     """decorator to mark function as deprecated

#     Args:
#         obj (Union[str, None, Callable], optional): Defaults to None.

#         Can operate in two configurations:\n
#         1. obj is the function that you want to deprecate\n
#         \t@deprecate\n
#         \tdef foo(...):\n
#         \t\t...\n\n
#         2. obj is an advise message\n
#         \t@deprecate("instead use ...")\n
#         \tdef foo(...):
#         \t\t...
#     """
#     from .Colors import warning
#     # if callable(obj):
#     if isinstance(obj, Callable):
#         @ functools.wraps(obj)
#         def wrapper(*args, **kwargs) -> Any:
#             warning(
#                 f"As marked by the developer, {obj.__module__}.{obj.__qualname__} is deprecated")
#             return obj(*args, **kwargs)
#         return wrapper

#     def deco(func: Callable) -> Callable:
#         @ functools.wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             warning(
#                 f"As marked by the developer, {func.__module__}.{func.__qualname__} is deprecated")
#             if obj:
#                 print(obj)
#             return func(*args, **kwargs)
#         return wrapper
#     return deco


@validate
def atomic(func: Callable) -> Callable:
    lock = threading.Lock()

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper


@validate
def limit_recursion(max_depth: int, return_value: Any = None, quiet: bool = True):
    """decorator to limit recursion of functions

    Args:
        max_depth (int): max recursion depth which is allowed for this function
        return_value (_type_, optional): The value to return when the limit is reached. Defaults to None.
            if is None, will return the last (args, kwargs)
        quiet (bool, optional): whether to print a warning message. Defaults to True.
    """

    from .Colors import warning

    def deco(func):
        @ functools.wraps(func)
        def wrapper(*args, **kwargs):
            depth = functools.reduce(
                lambda count, line:
                    count + 1 if re.search(f"{func.__name__}\(.*\)$", line)
                    else count,
                traceback.format_stack(), 0
            )
            if depth >= max_depth:
                if not quiet:
                    warning(
                        f"limit_recursion has limited the number of calls for {func.__module__}.{func.__qualname__} to {max_depth}")
                if return_value:
                    return return_value
                return args, kwargs
            return func(*args, **kwargs)
        return wrapper
    return deco


@validate
def timeout(timeout: int | float) -> Callable:
    """A decorator to limit runtime for a function

    Args:
        timeout (int | float): allowed runtime duration

    Raises:
        thread_error: if there is a thread related error
        function_error: if there is an error in the decorated function

    Returns:
        Callable: The decorated function
    """
    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {timeout} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as function_error:
                    res[0] = function_error

            t = threading.Thread(target=timeout_wrapper, daemon=True)
            try:
                t.start()
                t.join(timeout)
            except Exception as thread_error:
                raise thread_error
            if isinstance(res[0], BaseException):
                raise res[0]
            return res[0]
        return wrapper
    return timeout_deco


@validate
def attach(before: Callable = None, after: Callable = None) -> Callable:
    if before is None and after is None:
        raise ValueError("You must supply at least one function")

    def attach_deco(func: Callable):
        if not isinstance(func, Callable):
            raise ValueError("attach must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if before is not None:
                before()
            res = func(*args, **kwargs)
            if after is not None:
                after()
            return res
        return wrapper
    return attach_deco


__all__ = [
    "validate",
    "NotImplemented",
    "PartiallyImplemented",
    "memo",
    "overload",
    "abstractmethod",
    # "virtual",
    # "override",
    # "deprecate",
    "atomic",
    "limit_recursion",
    "timeout",
    "attach"

]
