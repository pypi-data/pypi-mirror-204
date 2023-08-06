from jax import jit
from jax.numpy import minimum
from .vjp.identity import identity
from .relu import relu


@jit
@identity
def relu1(x):
    return minimum(relu(x), 1)
