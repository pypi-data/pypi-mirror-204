from jax import jit
from .vjp.identity import identity
from .binary import binary
from .relu1 import relu1


@jit
@identity
def brelu1(x):
    return binary(x) + relu1(x)
