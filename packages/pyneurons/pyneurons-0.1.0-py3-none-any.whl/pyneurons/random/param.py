from jax.random import normal


def param(key, shape):
    return normal(key, shape) * 0.1
