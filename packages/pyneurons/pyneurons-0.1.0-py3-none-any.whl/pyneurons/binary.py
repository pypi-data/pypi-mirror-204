from jax import jit
from jax.numpy import heaviside
from .vjp.identity import identity


@jit
@identity
def binary(x):
    return heaviside(x, 1)
