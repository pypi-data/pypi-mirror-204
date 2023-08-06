from jax import jit


@jit
def apply(neuron, x):
    w, b = neuron
    return (x @ w) + b
