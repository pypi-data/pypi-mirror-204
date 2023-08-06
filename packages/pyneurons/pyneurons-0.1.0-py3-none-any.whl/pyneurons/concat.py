from functools import partial
from jax.numpy import concatenate
from .implode import implode


def concat(pytrees):
    return implode(partial(concatenate, axis=-1), pytrees)
