from jax.numpy import stack as stack_function
from .implode import implode


def stack(pytrees):
    return implode(stack_function, pytrees)
