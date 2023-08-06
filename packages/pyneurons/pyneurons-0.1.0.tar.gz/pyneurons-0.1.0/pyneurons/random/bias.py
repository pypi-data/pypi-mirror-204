from jax.numpy import negative
from .weight import weight


def bias(*args, **kwargs):
    return negative(weight(*args, **kwargs))
