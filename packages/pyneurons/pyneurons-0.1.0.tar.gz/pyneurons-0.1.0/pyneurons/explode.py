from functools import partial
from contextlib import suppress
from jax.tree_util import tree_flatten, tree_unflatten


def explode(function, pytree):
    leaves, treedef = tree_flatten(pytree)
    entries = list(map(function, leaves))
    entries = list(consume(entries))
    return list(map(partial(tree_unflatten, treedef), entries))


def shift(a):
    return a.pop(0)


def consume(entries):
    with suppress(IndexError):
        while True:
            yield list(map(shift, entries))
