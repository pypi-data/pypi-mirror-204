from functools import partial
from jax.tree_util import tree_map
from jax import grad, jit
from .loss import loss
from .gd import gd


@jit
def fit(model, x, y, learning_rate=0.1):
    gradient = grad(loss)(model, x, y)
    return tree_map(partial(gd, learning_rate), model, gradient)
