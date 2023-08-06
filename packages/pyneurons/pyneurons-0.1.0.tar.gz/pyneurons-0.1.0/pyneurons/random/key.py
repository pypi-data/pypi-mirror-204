from jax.random import PRNGKey
from .seed import seed


def key():
    return PRNGKey(seed())
