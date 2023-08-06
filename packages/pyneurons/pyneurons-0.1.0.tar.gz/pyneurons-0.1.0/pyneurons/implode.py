from jax.tree_util import tree_map


def implode(function, pytrees):
    return tree_map(lambda *leaves: function(list(leaves)), *pytrees)
