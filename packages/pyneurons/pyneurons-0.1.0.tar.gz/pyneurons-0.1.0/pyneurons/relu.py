from jax import jit
from jax.numpy import maximum
from .vjp.identity import identity


@jit
@identity
def relu(x):
    return maximum(x, 0)
