from jax.tree_util import register_pytree_node_class


@register_pytree_node_class
class Box(tuple):
    def __new__(cls, x):
        return super().__new__(cls, (x,))

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_pytree_node_class(cls)

    def tree_flatten(self):
        (x,) = self
        return (x,), None

    @classmethod
    def tree_unflatten(cls, _, children):
        (x,) = children
        return cls(x)
