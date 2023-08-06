from collections.abc import Callable
from multipledispatch import dispatch
from .identity import identity
from .model import Model
from .box import Box


@dispatch(str, Callable, Callable)
def bind(name, constructor, apply):
    return type(name, (Model,), {"constructor": constructor, "apply": apply})


@dispatch(Callable, Callable)
def bind(constructor, apply):
    return bind(Model.__name__, constructor, apply)


@dispatch(object, Callable)
def bind(x, apply):
    cls = bind(identity, apply)
    return cls(Box(x))
