from jax.numpy import split as split_function
from .explode import explode


def split(pytree):
    return explode(
        lambda array: split_function(array, array.shape[-1], axis=-1), pytree
    )
