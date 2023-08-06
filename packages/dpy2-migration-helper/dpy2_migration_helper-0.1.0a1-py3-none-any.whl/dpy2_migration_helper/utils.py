import ast
import functools
from typing import Callable, Optional

from typing_extensions import ParamSpec

_P = ParamSpec("_P")


def single_visitor(func: Callable[_P, None]) -> Callable[_P, None]:
    @functools.wraps(func)
    def wrapped(*args: _P.args, **kwargs: _P.kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError:
            return None

    return wrapped


def get_poskwarg(
    call: ast.Call, position: Optional[int] = None, keyword_name: Optional[str] = None
) -> Optional[ast.AST]:
    if position is not None and position < len(call.args):
        return call.args[position]

    for keyword in call.keywords:
        if keyword.arg == keyword_name:
            return keyword.value

    return None
