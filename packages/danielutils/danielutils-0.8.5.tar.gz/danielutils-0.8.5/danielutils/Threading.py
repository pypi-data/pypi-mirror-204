# although it's related to threading, atomic decorator implemented at .Decorators
import threading
import functools
from typing import Callable


def threadify(func: Callable) -> Callable:
    """will modify the function that when calling it a new thread will start to run it

    Args:
        func (Callable): the function to make a thread

    Returns:
        Callable: the modified function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
    return wrapper


__all__ = [
    "threadify"
]
